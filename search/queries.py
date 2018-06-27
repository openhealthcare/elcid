"""
Allow us to make search queries
"""
import datetime
from django.db.models import Max, Min
from django.conf import settings

from opal import models
from opal.utils import stringport
from search.search_rules import SearchRule


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

    def get_patient_summaries(self, patients):
        raise NotImplementedError()

    def sort_patients(self, patients):
        raise NotImplementedError()


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
        rule_name = criteria['rule']
        search_rule = SearchRule.get_rule(rule_name, self.user)
        return search_rule.query(criteria)

    def get_patients(self):
        episodes = self.get_episodes()
        patient_ids = set([i.patient_id for i in episodes])
        return self.sort_patients(
            models.Patient.objects.filter(id__in=patient_ids)
        )

    def sort_patients(self, patients):
        patients = patients.annotate(
            max_episode_id=Max('episode__id')
        )
        return patients.order_by("-max_episode_id")

    def get_patient_summary(self, patient):
        result = dict()
        demographics = patient.demographics_set.first()
        for i in ["first_name", "surname", "hospital_number", "date_of_birth"]:
            result[i] = getattr(demographics, i)
        result["start"] = patient.episode_set.aggregate(
            min_start=Min('start')
        )["min_start"]

        result["end"] = patient.episode_set.aggregate(
            max_end=Max('end')
        )["max_end"]

        result["count"] = patient.episode_set.count()
        result["patient_id"] = patient.id
        result["categories"] = list(patient.episode_set.order_by(
            "category_name"
        ).values_list(
            "category_name", flat=True
        ))
        return result

    def get_patient_summaries(self, patients):
        patients.prefetch_related("demographics")
        return [self.get_patient_summary(patient) for patient in patients]

    def _episodes_without_restrictions(self):
        all_matches = [
            (query_row['combine'], self.episodes_for_criteria(query_row))
            for query_row in self.query
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

    def description(self):
        """
        Provide a textual description of the current search
        """
        line_description = []

        for query_line in self.query:
            search_rule = SearchRule.get_rule(query_line["rule"], self.user)
            line_description.append(
                search_rule.get_query_description(query_line)
            )

        joiner = "\n{} ".format(self.query[0]["combine"])
        filters = joiner.join(line_description)

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
