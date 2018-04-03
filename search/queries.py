"""
Allow us to make search queries
"""
import datetime
from django.db.models import Max
from django.conf import settings

from opal import models
from opal.core import subrecords
from opal.utils import stringport
from search.search_rule import SearchRule


def get_model_name_from_column_name(column_name):
    return column_name.replace(' ', '').replace('_', '').lower()


def get_model_from_api_name(column_name):
    if column_name == "tagging":
        return models.Tagging
    else:
        return subrecords.get_subrecord_from_api_name(column_name)


class PatientSummary(object):
    def __init__(self, episode):
        self.start = episode.start
        self.end = episode.end
        self.episode_ids = set([episode.id])
        self.patient_id = episode.patient.id
        self.categories = set([episode.category_name])
        self.id = episode.patient.demographics_set.get().id

    def update(self, episode):
        if not self.start:
            self.start = episode.start
        elif episode.start:
            if self.start > episode.start:
                self.start = episode.start

        if not self.end:
            self.end = episode.end
        elif episode.end:
            if self.end < episode.end:
                self.end = episode.end

        self.episode_ids.add(episode.id)
        self.categories.add(episode.category_name)

    def to_dict(self):
        result = {k: getattr(self, k) for k in [
            "patient_id", "start", "end", "id"
        ]}
        result["categories"] = sorted(self.categories)
        result["count"] = len(self.episode_ids)
        return result


def episodes_for_user(episodes, user):
    """
    Given an iterable of EPISODES and a USER, return a filtered
    list of episodes that this user has the permissions to know
    about.
    """
    return [e for e in episodes if e.visible_to(user)]


class QueryBackend(object):
    """
    Base class for search implementations to inherit from
    """
    def __init__(self, user, query):
        self.user = user
        self.query = query

    def fuzzy_query(self):
        raise NotImplementedError()

    def get_episodes(self):
        raise NotImplementedError()

    def description(self):
        raise NotImplementedError()

    def get_patients(self):
        raise NotImplementedError()

    def get_patient_summaries(self):
        raise NotImplementedError()

    def patients_as_json(self):
        patients = self.get_patients()
        return [
            p.to_dict(self.user) for p in patients
        ]


class DatabaseQuery(QueryBackend):
    """
    The default built in query backend for OPAL allows advanced search
    criteria building.

    We broadly map reduce all criteria then the set of combined and/or
    criteria together, then only unique episodes.

    Finally we filter based on episode type level restrictions.
    """

    def fuzzy_query(self):
        """
        Fuzzy queries break apart the query string by spaces and search a
        number of fields based on the underlying tokens.

        We then search hospital number, first name and surname by those fields
        and order by the occurances

        so if you put in Anna Lisa, even though this is a first name split
        becasuse Anna and Lisa will both be found, this will rank higher
        than an Anna or a Lisa, although both of those will also be found

        it returns a list of patients ordered by their most recent episode id
        """
        some_query = self.query
        patients = models.Patient.objects.search(some_query)
        patients = patients.annotate(
            max_episode_id=Max('episode__id')
        )
        return patients.order_by("-max_episode_id")

    def episodes_for_criteria(self, criteria):
        """
        Given one set of criteria, return episodes that match it.
        """
        column_name = criteria['column']
        search_rule = SearchRule.get(column_name)
        return search_rule.query(criteria)

    def get_aggregate_patients_from_episodes(self, episodes):
        # at the moment we use start/end only
        patient_summaries = {}

        for episode in episodes:
            patient_id = episode.patient_id
            if patient_id in patient_summaries:
                patient_summaries[patient_id].update(episode)
            else:
                patient_summaries[patient_id] = PatientSummary(episode)

        patients = models.Patient.objects.filter(
            id__in=list(patient_summaries.keys())
        )
        patients = patients.prefetch_related("demographics_set")

        results = []

        for patient_id, patient_summary in patient_summaries.items():
            patient = next(p for p in patients if p.id == patient_id)
            demographic = patient.demographics_set.get()

            result = {k: getattr(demographic, k) for k in [
                "first_name", "surname", "hospital_number", "date_of_birth"
            ]}

            result.update(patient_summary.to_dict())
            results.append(result)

        return results

    def _episodes_without_restrictions(self):
        all_matches = [
            (q['combine'], self.episodes_for_criteria(q))
            for q in self.query
        ]
        if not all_matches:
            return []

        working = set(all_matches[0][1])
        rest = all_matches[1:]

        for combine, episodes in rest:
            methods = {
                'and': 'intersection',
                'or' : 'union',
                'not': 'difference'
            }
            working = getattr(set(episodes), methods[combine])(working)

        return working

    def get_episodes(self):
        return episodes_for_user(
            self._episodes_without_restrictions(), self.user)

    def get_patient_summaries(self):
        eps = self._episodes_without_restrictions()
        episode_ids = [e.id for e in eps]

        # get all episodes of patients, that have episodes that
        # match the criteria
        all_eps = models.Episode.objects.filter(
            patient__episode__in=episode_ids
        )
        filtered_eps = episodes_for_user(all_eps, self.user)
        return self.get_aggregate_patients_from_episodes(filtered_eps)

    def get_patients(self):
        patients = set(e.patient for e in self.get_episodes())
        return list(patients)

    def description(self):
        """
        Provide a textual description of the current search
        """
        filter_item_first_line = "{subrecord} {field} {queryType} {query}"
        filter_item = "{combine} {subrecord} {field} {queryType} {query}"
        line_description = []

        for idx, query_line in enumerate(self.query):
            search_rule = SearchRule.get(query_line["column"])
            display_name = search_rule.get_display_name()
            search_rule_field = search_rule.get_field(query_line["field"])
            field_display_name = search_rule_field.get_display_name()

            if idx == 0:
                template = filter_item_first_line
            else:
                template = filter_item
            line_description.append(
                template.format(
                    subrecord=display_name,
                    field=field_display_name,
                    queryType=query_line["queryType"],
                    query=query_line["query"],
                    combine=query_line["combine"]
                )
            )

        filters = "\n".join(line_description)

        complete_description = "{username} ({date})\nSearching for:\n{filters}"
        return complete_description.format(
            username=self.user.username,
            date=datetime.datetime.now().strftime(
                settings.DATETIME_INPUT_FORMATS[0]
            ),
            filters=filters
        )


def create_query(user, criteria):
    """
        gives us a level of indirection to select the search backend we're
        going to use, without this we can get import errors if the module is
        loaded after this module
    """
    if hasattr(settings, "OPAL_SEARCH_BACKEND"):
        query_backend = stringport(settings.OPAL_SEARCH_BACKEND)
        return query_backend(user, criteria)

    return DatabaseQuery(user, criteria)
