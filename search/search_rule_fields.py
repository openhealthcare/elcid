from django.db import models as djangomodels
from opal.core.fields import ForeignKeyOrFreeText
from django.utils.encoding import force_str
from opal.core import fields
from opal.utils import camelcase_to_underscore
from opal import models
from search.exceptions import SearchException
from search import model_queries

"""
    A search rule field is a field declared by a search rule.

    For model search rules, if a search rule is not explicitly
    declared in the search rule's `fields` attr then we
    wrap a model field in a ModelSearchRuleField

    the publish api used is...

    get_slug, the name of the field
    to_dict, the serialised version of the field in the schema
    query, the dictionary that the rule receives
"""


class SearchRuleField(object):
    lookup_list = None
    enum = None
    description = None
    slug = None
    display_name = None

    @classmethod
    def get_slug(klass):
        if klass.slug is not None:
            return klass.slug

        if klass.display_name is None:
            raise ValueError(
                'Must set display_name for {0}'.format(klass)
            )
        return camelcase_to_underscore(klass.display_name).replace(' ', '')

    def get_display_name(self):
        return self.display_name

    def get_description(self):
        return self.description

    def to_dict(self):
        return dict(
            name=self.get_slug(),
            title=self.display_name,
            type=self.field_type,
            enum=self.enum,
            type_display_name=self.type_display_name,
            lookup_list=self.lookup_list,
            description=self.description
        )

    def query(self, given_query):
        """
            takes in the full query and returns a list of episodes
        """
        raise NotImplementedError("please implement a query")


FIELD_TYPE_TO_QUERY = {
    fields.ForeignKeyOrFreeText: model_queries.query_for_fkorft_fields,
    djangomodels.BooleanField: model_queries.query_for_boolean_fields,
    djangomodels.DateField: model_queries.query_for_date_fields,
    djangomodels.ManyToManyField: model_queries.query_for_many_to_many_fields
}


class ModelSearchRuleField(SearchRuleField):
    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name

    @property
    def field(self):
        if isinstance(
            getattr(self.model, self.field_name), fields.ForeignKeyOrFreeText
        ):
            return getattr(self.model, self.field_name)
        return self.model._meta.get_field(self.field_name)

    @property
    def model_name(self):
        return self.model.__name__.lower()

    def to_dict(self):
        return self.model.build_schema_for_field_name(self.field_name)

    def get_slug(self):
        return self.field_name

    def get_display_name(self):
        return self.model._get_field_title(self.field_name)

    def get_description(self):
        field = self.field
        description = self.description

        if description:
            return description

        enum = self.model.get_field_enum(self.field_name)

        if enum:
            return "One of {}".format(", ".join([force_str(e) for e in enum]))

        related_fields = (
            models.ForeignKey, models.ManyToManyField,
        )

        if isinstance(field, fields.ForeignKeyOrFreeText):
            t = "Text"

        if isinstance(field, related_fields):
            if isinstance(field, models.ForeignKey):
                t = "One of the {}"
            else:
                t = "Some of the {}"
            related = field.rel.to
            return t.format(related._meta.verbose_name_plural.title())

    def get_model_query_args(self, query):
        """
            if we wanted all conditions in diagnosis beginning with C
            the model would be diagnosis
            the field_name would be condition
            the query_type would be beginning with
            the value would be 'C'
        """
        return dict(
            model=self.model,
            field_name=self.field_name,
            query_type=query["queryType"],
            value=query["query"]
        )

    def query(self, query):
        for field_type, query_method in FIELD_TYPE_TO_QUERY.items():
            if isinstance(self.field, field_type):
                return query_method(
                    **self.get_model_query_args(query)
                )
        if fields.is_numeric(self.field):
            return self.query_for_number_fields(
                **self.get_model_query_args(query)
            )

        elif isinstance(
            self.field, (djangomodels.CharField, djangomodels.TextField,)
        ):
            return model_queries.query_for_text_fields(
                **self.get_model_query_args(query)
            )
        else:
            raise NotImplementedError("we do not support this")


class EpisodeTeam(SearchRuleField):
    ALL_OF = "All Of"
    ANY_OF = "Any Of"

    display_name = "Team"
    description = "The team(s) related to an episode of care"
    field_type = "many_to_many_multi_select"
    type_display_name = "Text Field"

    @property
    def enum(self):
        return [i["title"] for i in models.Tagging.build_field_schema()]

    def translate_titles_to_names(self, titles):
        result = []
        titles_not_found = set(titles)
        for schema in models.Tagging.build_field_schema():
            if schema["title"] in titles:
                result.append(schema["name"])
                titles_not_found.remove(schema["title"])

        if titles_not_found:
            raise SearchException(
                "unable to find the tag titled {}".format(
                    ",".join(titles_not_found)
                )
            )
        return result

    def query(self, given_query):
        query_type = given_query["queryType"]
        team_display_names = given_query['query']
        if not query_type == self.ALL_OF:
            if not query_type == self.ANY_OF:
                err = """
                    unrecognised query type for the episode team query with {}
                """.strip()
                raise SearchException(err.format(query_type))

        team_names = self.translate_titles_to_names(team_display_names)
        qs = models.Episode.objects.all()
        if given_query["queryType"] == self.ALL_OF:
            for team_name in team_names:
                qs = qs.filter(tagging__value=team_name)
        else:
            qs = qs.filter(tagging__value__in=team_names)

        return qs.distinct()
