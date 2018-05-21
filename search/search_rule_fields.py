from django.core.urlresolvers import reverse
from opal import models
from opal.core import fields
from opal.core import serialization
from search.exceptions import SearchException
from search import subrecord_queries
from search import subrecord_discoverable

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


class SearchRuleField(subrecord_discoverable.SubrecordFieldWrapper):
    # the description of the widget as shown on the right hand side
    widget_description = GENERIC_WIDGET_DESCRIPTION

    # the description of the query the user has selected when it is
    # shown at the top
    description_template = None

    # the arguments that are required for this query
    query_args = ["value", "query_type"]

    def get_description_template(self):
        if self.description_template:
            return self.description_template
        return "search/field_descriptions/generic.html"

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
    description_template = "search/field_descriptions/boolean.html"


class NumberSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/number.html"
    query_method = staticmethod(subrecord_queries.query_for_number_fields)
    description_template = "search/field_descriptions/number.html"


class DateSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/date.html"
    query_method = staticmethod(subrecord_queries.query_for_date_fields)

    def get_description_template(self):
        if subrecord_discoverable.is_date_time_field(
            self.field
        ):
            return "search/field_descriptions/date_time.html"
        return "search/field_descriptions/date.html"


class SelectSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/text.html"
    query_method = staticmethod(
        subrecord_queries.query_for_many_to_many_fields
    )


class TextSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/text.html"
    widget_description = "partials/search/descriptions/text.html"
    query_method = staticmethod(subrecord_queries.query_for_text_fields)
    description_template = "search/field_descriptions/text.html"


class FkOrFtSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/text.html"
    widget_description = "partials/search/descriptions/text.html"
    query_method = staticmethod(subrecord_queries.query_for_fk_or_ft_fields)
    description_template = "search/field_descriptions/text.html"


class TimeSearchRuleField(ModelSearchRuleField):
    widget = "search/widgets/time.html"
    query_method = staticmethod(subrecord_queries.query_for_time_fields)


FIELD_TYPE_TO_SEARCH_RULE_FIELD = {
    subrecord_discoverable.is_foreign_key_or_free_text: FkOrFtSearchRuleField,
    fields.is_numeric: NumberSearchRuleField,
    subrecord_discoverable.is_boolean: BooleanSearchRuleField,
    subrecord_discoverable.is_many_to_many_field: SelectSearchRuleField,
    subrecord_discoverable.is_date_field: DateSearchRuleField,
    subrecord_discoverable.is_text: TextSearchRuleField,
    subrecord_discoverable.is_time_field: TimeSearchRuleField,
    subrecord_discoverable.is_select: SelectSearchRuleField,
}


class EpisodeDateQuery(object):
    def query(self, given_query):
        query_type = given_query["query_type"]
        if query_type not in {"Before", "After"}:
            raise SearchException(
                "Date queries required before or after to be declared"
            )

        value = serialization.deserialize_date(given_query["value"])
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
    description_template = "search/field_descriptions/date.html"


class EpisodeEnd(
    EpisodeDateQuery, SearchRuleField
):
    type_display_name = "Date"
    description = "The date the episode ended"
    field_name = "end"
    display_name = "End"
    widget = "search/widgets/date.html"
    description_template = "search/field_descriptions/date.html"


class EpisodeTeam(
    SearchRuleField
):
    ALL_OF = "All Of"
    ANY_OF = "Any Of"
    display_name = "Team"
    description = ""
    type_display_name = "Text Field"
    field_name = "team"
    widget = "search/widgets/team_many_to_many.html"
    widget_description = "partials/search/descriptions/many_to_many.html"
    description_template = "search/field_descriptions/episode/team.html"

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
