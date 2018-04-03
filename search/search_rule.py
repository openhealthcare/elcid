from opal.core.discoverable import DiscoverableFeature
from opal.core import subrecords
from opal.models import Episode
from search.search_rule_fields import ModelSearchRuleField, EpisodeTeam
from search.exceptions import SearchException

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


class SearchRule(DiscoverableFeature):
    module_name = "search_rule"
    fields = []
    display_name = ""

    def get_fields(self):
        for field in self.fields:
            yield field()

    def get_field(self, field_api_name):
        return next(
            i for i in self.get_fields() if i.get_slug() == field_api_name
        )

    def to_search_dict(self):
        return dict(
            name=self.get_slug(),
            display_name=self.display_name,
            fields=[i.to_dict() for i in self.get_fields()],
            description=getattr(self, "description", None)
        )

    def to_extract_dict(self):
        return self.to_search_dict()

    def get_display_name(self):
        return self.display_name

    @classmethod
    def get(klass, name):
        """
        Return a specific subclass by slug
        """
        for sub in klass.list():
            if sub.get_slug() == name:
                return sub

    @classmethod
    def list(klass):
        search_rules = super(SearchRule, klass).list()
        search_rule_slugs = set()

        for search_rule in search_rules:
            search_rule_slugs.add(search_rule.get_slug())
            yield search_rule()

        for subrecord in subrecords.subrecords():
            if subrecord.get_api_name() not in search_rule_slugs:
                if subrecord._advanced_searchable:
                    yield ModelSearchRule(subrecord)

    def query(self, given_query):
        given_field = given_query['field']
        query_field = next(
            f for f in self.get_fields() if f.get_slug() == given_field
        )
        return query_field.query(given_query)


class ModelSearchRule(object):
    description = ""
    fields = []

    def __init__(self, model=None):
        if model:
            self.model = model
        if not self.model:
            raise SearchException(
                "A model search rule either needs to be instantiated with a \
model, or have one on the class"
            )

    def get_slug(self):
        return self.model.get_api_name()

    def get_display_name(self):
        return getattr(
            self, "display_name", self.model.get_display_name()
        )

    def get_fields(self):
        """
            If we've got fields declared, returned them.
        """
        fields = self.fields

        if not fields:
            fields = self.model._get_fieldnames_to_serialize()

        for field in fields:
            if isinstance(field, (str, unicode,)):
                yield ModelSearchRuleField(self.model, field)
            else:
                yield field()

    def get_search_fields_schema(self):
        fields = self.model.build_field_schema()
        for field in fields:
            field["type_display_name"] = self.model.get_human_readable_type(
                field["name"]
            )
        return sorted(
            fields, key=lambda x: x["title"]
        )

    def to_extract_dict(self):
        """
            Get the schema of extract fields.

            For example we want to remove the users personal information.
        """
        search_dict = self.to_search_dict()
        field_names = self.model._get_fieldnames_to_extract()
        search_dict["fields"] = [
            i for i in search_dict["fields"] if i["name"] in field_names
        ]
        return search_dict

    def to_search_dict(self):
        """
            Get the schema of search fields
        """
        serialised = {
            'name': self.model.get_api_name(),
            'display_name': self.model.get_display_name(),
            'description': self.description
        }

        fields = self.get_search_fields_schema()

        if hasattr(self.model, 'get_icon'):
            serialised["icon"] = self.model.get_icon()
        for field in fields:
            field["type_display_name"] = self.model.get_human_readable_type(
                field["name"]
            )
        serialised["fields"] = fields
        return serialised

    def get_field(self, field_name):
        for i in self.get_fields():
            if i.get_slug() == field_name:
                return i
        raise SearchException("Unable to find field {} for {}".format(
            field_name, self.get_display_name()
        ))

    def query(self, some_query):
        given_field = some_query['field']
        for i in self.get_fields():
            if i.get_slug() == given_field:
                return i.query(some_query)
        raise SearchException("Unable to find field {} for {}".format(
            given_field, self.get_display_name()
        ))


class EpisodeQuery(ModelSearchRule):
    display_name = "Episode"
    slug = "episode"
    model = Episode
    fields = (EpisodeTeam, Episode.start, Episode.end)
