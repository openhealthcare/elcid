import itertools
from opal.core.discoverable import DiscoverableFeature
from opal import models
from elcid import models as emodels
from search.subrecord_discoverable import SubrecordDiscoverableMixin
from search import search_rule_fields

"""
    A Search Rule a
    A Search Rule is roughly similar to a rest framework serialiser
    with bits...

    What we want is a discoverable that will return a search rule if its
    set or a model wrapped in a search field if its not.

    Similar to a Step in a pathway.

    Fields are declared on the search rule or default to all.

    A search rule field takes in a query, and is serialised to an extract.

    stage 1.
    Just do the wrap.

    stage 2.
    Manage the serialisation.
"""


class SearchRule(
    SubrecordDiscoverableMixin, DiscoverableFeature
):
    module_name = "search_rules"
    FIELDS_TO_IGNORE = {
        "id",
        "created",
        "updated",
        "created_by_id",
        "updated_by_id",
        "consistency_token",
        "episode_id",
        "patient_id"
    }

    def cast_field_name_to_attribute(self, str):
        return search_rule_fields.ModelSearchRuleField(self.model, str)

    def get_description(self):
        return getattr(self, "description", "")

    def get_model_fields(self):
        result = self.model._get_fieldnames_to_serialize()
        result = [i for i in result if i not in self.FIELDS_TO_IGNORE]
        if issubclass(self.model, models.PatientSubrecord):
            result = [i for i in result if not i == "patient"]

        if issubclass(self.model, models.EpisodeSubrecord):
            result = [i for i in result if not i == "episode"]
        return result

    def query(self, given_query):
        given_field = given_query['field']
        query_field = self.get_field(given_field)
        return query_field.query(given_query)

    def get_widgets(self):
        for i in self.get_fields():
            yield i.get_widget()

    def get_widget_descriptions(self):
        for i in self.get_fields():
            yield i.get_widget_description()

    @classmethod
    def widgets(cls, user):
        all_widgets = (i.get_widgets() for i in cls.list(user))
        return {i for i in itertools.chain(
            *all_widgets
        )}

    @classmethod
    def widget_descriptions(cls, user):
        widget_descriptions = (
            i.get_widget_descriptions() for i in cls.list(user)
        )
        return {i for i in itertools.chain(
            *widget_descriptions
        )}


class EpisodeQuery(SearchRule):
    display_name = "Episode"
    slug = "episode"
    model = models.Episode
    fields = (
        search_rule_fields.EpisodeTeam,
        search_rule_fields.EpisodeStart,
        search_rule_fields.EpisodeEnd
    )


class ResultQuery(SearchRule):
    exclude = True
    slug = emodels.Result.get_api_name()


class DuplicatePatientQuery(SearchRule):
    exclude = True
    slug = emodels.DuplicatePatient.get_api_name()