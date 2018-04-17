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


class SearchRule(SubrecordDiscoverableMixin, DiscoverableFeature):
    module_name = "search_overrides"
    fields = None
    display_name = ""
    slug = ""

    def cast_field_name_to_attribute(self, str):
        return search_rule_fields.ModelSearchRuleField(self.model, str)

    def get_description(self):
        return getattr(self, "description", "")

    def get_model_fields(self):
        return self.model._get_fieldnames_to_serialize()

    def query(self, given_query):
        given_field = given_query['field']
        query_field = self.get_field(given_field)
        return query_field.query(given_query)


class EpisodeQuery(SearchRule):
    display_name = "Episode"
    slug = "episode"
    model = models.Episode
    fields = (search_rule_fields.EpisodeTeam, "start", "end")


class ResultQuery(SearchRule):
    exclude = True
    slug = emodels.Result.get_api_name()
