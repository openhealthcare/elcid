from django.db import models as djangomodels
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
    widget_description = GENERIC_WIDGET_DESCRIPTION
    description_template = "search/description.html"

    def get_description_template(self):
        return self.description_template

    def query(self, given_query):
        """
            takes in the full query and returns a list of episodes
        """
        raise NotImplementedError("please implement a query")

    def get_widget(self):
        return self.widget

    def get_widget_description(self):
        return self.widget_description

    def to_dict(self):
        result = super(SearchRuleField, self).to_dict()
        result["widget"] = self.get_widget()
        result["widget_description"] = self.get_widget_description()
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


FIELD_TYPE_TO_QUERY = {
    is_foreign_key_or_free_text: subrecord_queries.query_for_fkorft_fields,
    fields.is_numeric: subrecord_queries.query_for_number_fields,
    is_boolean: subrecord_queries.query_for_boolean_fields,
    is_many_to_many_field: subrecord_queries.query_for_many_to_many_fields,
    is_date_field: subrecord_queries.query_for_date_fields,
    is_text: subrecord_queries.query_for_text_fields,
    is_select: subrecord_queries.query_for_related_fields
}

FIELD_TYPE_TO_WIDGET = {
    is_foreign_key_or_free_text: "search/widgets/text.html",
    fields.is_numeric: "search/widgets/number.html",
    is_boolean: "search/widgets/boolean.html",
    is_many_to_many_field: "search/widgets/text.html",
    is_date_field: "search/widgets/date.html",
    is_text: "search/widgets/text.html",
    is_select: "search/widgets/select.html",
}

WIDGET_TO_DESCRIPTION = {
    "search/widgets/text.html": "partials/search/descriptions/text.html",
    "search/widgets/number.html": GENERIC_WIDGET_DESCRIPTION,
    "search/widgets/many_to_many.html": "partials/search/descriptions/many_to_many.html",
    "search/widgets/select.html": GENERIC_WIDGET_DESCRIPTION,
    "search/widgets/number.html": GENERIC_WIDGET_DESCRIPTION,
    "search/widgets/date.html": GENERIC_WIDGET_DESCRIPTION,
    "search/widgets/boolean.html": "partials/search/descriptions/boolean.html"
}


class ModelSearchRuleField(SearchRuleField):
    widget = None

    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name

    def get_model_query_args(self, query):
        """
            if we wanted all conditions in diagnosis beginning with C
            the model would be diagnosis
            the field_name would be condition
            the query_type would be beginning with
            the value would be 'C'
        """
        query_args = {
            i: v for i, v in query.items() if i not in {
                "column", "field", "combine"
            }
        }
        query_args["value"] = query_args.pop("query")
        if "queryType" in query_args:
            query_type = query_args.pop("queryType")
            query_args["query_type"] = query_type
        return dict(
            model=self.model,
            field_name=self.field_name,
            **query_args
        )

    def get_widget_description(self):
        return WIDGET_TO_DESCRIPTION[self.get_widget()]

    def query(self, query):
        for field_type_method, query_method in FIELD_TYPE_TO_QUERY.items():
            if field_type_method(self.field):
                return query_method(
                    **self.get_model_query_args(query)
                )
        raise NotImplementedError("we cannot query this {}".format(
            self.field.__class__
        ))

    def get_widget(self):
        if self.widget:
            return self.widget
        for field_type_method, widget in FIELD_TYPE_TO_WIDGET.items():
            if field_type_method(self.field):
                return widget

        raise NotImplementedError(
            "we do not have a widget for {} {}".format(
                self.field, self.field.__class__
            )
        )


class EpisodeDateQuery(object):
    def query(self, given_query):
        query_type = given_query["queryType"]
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
    widget_description = WIDGET_TO_DESCRIPTION[
        "search/widgets/many_to_many.html"
    ]

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
