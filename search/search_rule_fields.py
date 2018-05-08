from django.db import models as djangomodels
from django.core.urlresolvers import reverse
from opal.core import fields
from opal import models
from opal.core import serialization
from search.exceptions import SearchException
from search import subrecord_queries
from search.subrecord_discoverable import SubrecordFieldWrapper

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
GENERIC_WIDGET_DESCRIPTION = "partials/search/descriptions/widget_description.html"


class SearchRuleField(SubrecordFieldWrapper):
    # the description of the widget as shown on the right hand side
    widget_description = GENERIC_WIDGET_DESCRIPTION

    # the description of the query the user has selected when it is
    # shown at the top
    description_template = "partials/search/rule_description.html"

    # the arguments that are required for this query
    query_args = ["value", "query_type"]

    def get_description_template(self):
        return self.description_template

    def get_description_template_url(self, rule):
        return reverse('extract_query_description', kwargs=dict(
            rule_api_name=rule.get_api_name(),
            field_api_name=self.get_name()
        ))

    def query(self, given_query):
        """
            takes in the full query and returns a list of episodes
        """
        raise NotImplementedError("please implement a query")

    def get_widget(self):
        if not self.widget:
            raise SearchException(
                "{} requires a widget".format(self)
            )
        return self.widget

    def get_widget_description(self):
        return self.widget_description

    def get_query_args(self):
        return self.query_args

    def get_query_description(self, query):
        return "{} {} {}".format(
            self.get_display_name(),
            query["query_type"].lower(),
            query["value"]
        )

    def to_dict(self):
        result = super(SearchRuleField, self).to_dict()
        result["widget"] = self.get_widget()
        result["widget_description"] = self.get_widget_description()
        result["query_args"] = self.get_query_args()
        return result


def is_boolean(some_field):
    return isinstance(
        some_field, (djangomodels.BooleanField, djangomodels.NullBooleanField,)
    )


def is_text(some_field):
    return isinstance(
        some_field, (djangomodels.TextField, djangomodels.CharField,)
    )


def is_date_field(some_field):
    return isinstance(
        some_field, (djangomodels.DateField, djangomodels.DateTimeField,)
    )


def is_many_to_many_field(some_field):
    return isinstance(
        some_field, djangomodels.ManyToManyField
    )


def is_foreign_key_or_free_text(some_field):
    return isinstance(
        some_field, fields.ForeignKeyOrFreeText
    )


def is_select(some_field):
    return isinstance(
        some_field, djangomodels.ForeignKey
    )


class ModelSearchRuleField(SearchRuleField):
    query_method = None
    widget = None

    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name

    def query(self, query):
        query_args = self.get_query_args()
        query_params = {i: query[i] for i in query_args}
        query_params["model"] = self.model
        query_params["field_name"] = self.field_name
        return self.query_method(**query_params)


class BooleanSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/boolean.html"
    widget_description = "partials/search/descriptions/boolean.html"
    query_method = staticmethod(subrecord_queries.query_for_boolean_fields)
    query_args = ["value"]


class NumberSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/number.html"
    query_method = staticmethod(subrecord_queries.query_for_number_fields)


class DateSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/date.html"
    query_method = staticmethod(subrecord_queries.query_for_date_fields)


class SelectSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/text.html"
    query_method = staticmethod(
        subrecord_queries.query_for_many_to_many_fields
    )


class TextSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/text.html"
    widget_description = "partials/search/descriptions/text.html"
    query_method = staticmethod(subrecord_queries.query_for_text_fields)


class FkOrFtSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/text.html"
    widget_description = "partials/search/descriptions/text.html"
    query_method = staticmethod(subrecord_queries.query_for_fk_or_ft_fields)


FIELD_TYPE_TO_SEARCH_RULE_FIELD = {
    is_foreign_key_or_free_text: FkOrFtSearchRuleField,
    fields.is_numeric: NumberSearchRuleField,
    is_boolean: BooleanSearchRuleField,
    is_many_to_many_field: SelectSearchRuleField,
    is_date_field: DateSearchRuleField,
    is_text: TextSearchRuleField,
    is_select: SelectSearchRuleField,
}


class EpisodeDateQuery(object):
    def query(self, given_query):
        query_type = given_query["query_type"]
        if query_type not in {"Before", "After"}:
            raise SearchException(
                "Date queries required before or after to be declared"
            )

        value = serialization.deserialize_date(given_query["query"])
        if query_type == 'Before':
            qtype = '__lte'
        elif query_type == 'After':
            qtype = '__gte'
        return models.Episode.objects.filter(
            **{"{}{}".format(self.field_name, qtype): value}
        )


class EpisodeStart(
    EpisodeDateQuery, SearchRuleField
):
    type_display_name = "Date"
    description = "The date the episode started"
    field_name = "start"
    display_name = "Start"
    widget = "search/widgets/date.html"


class EpisodeEnd(
    EpisodeDateQuery, SearchRuleField
):
    type_display_name = "Date"
    description = "The date the episode ended"
    field_name = "end"
    display_name = "End"
    widget = "search/widgets/date.html"


class EpisodeTeam(
    SearchRuleField
):
    ALL_OF = "All Of"
    ANY_OF = "Any Of"
    display_name = "Team"
    description = "The team(s) related to an episode of care"
    type_display_name = "Text Field"
    field_name = "team"
    widget = "search/widgets/team_many_to_many.html"
    widget_description = "partials/search/descriptions/many_to_many.html"

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
        query_type = given_query["query_type"]
        team_display_names = given_query['value']
        if not query_type == self.ALL_OF:
            if not query_type == self.ANY_OF:
                err = """
                    unrecognised query type for the episode team query with {}
                """.strip()
                raise SearchException(err.format(query_type))

        team_names = self.translate_titles_to_names(team_display_names)
        qs = models.Episode.objects.all()
        if given_query["query_type"] == self.ALL_OF:
            for team_name in team_names:
                qs = qs.filter(tagging__value=team_name)
        else:
            qs = qs.filter(tagging__value__in=team_names)

        return qs.distinct()
