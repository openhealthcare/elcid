from django.db import models as djangomodels
from opal.core import fields
from opal import models
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


class SearchRuleField(SubrecordFieldWrapper):
    def query(self, given_query):
        """
            takes in the full query and returns a list of episodes
        """
        raise NotImplementedError("please implement a query")

    def get_widget(self):
        return self.widget


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
    is_many_to_many_field: "search/widgets/many_to_many.html",
    is_date_field: "search/widgets/date.html",
    is_text: "search/widgets/text.html",
    is_select: "search/widgets/select.html",
}


class ModelSearchRuleField(SearchRuleField):
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
        return dict(
            model=self.model,
            field_name=self.field_name,
            query_type=query["queryType"],
            value=query["query"]
        )

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
        for field_type_method, widget in FIELD_TYPE_TO_WIDGET.items():
            if field_type_method(self.field):
                return widget

        raise NotImplementedError(
            "we do not have a widget for {} {}".format(
                self.field, self.field.__class__
            )
        )

    def to_dict(self):
        result = super(ModelSearchRuleField, self).to_dict()
        result["widget"] = self.get_widget()
        return result


class EpisodeDateQuery(object):
    def query(self, given_query):
        query_type = given_query["queryType"]
        value = models.deserialize_date(given_query["query"])
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
    type = "date"
    type_display_name = "Date"
    description = "The date the episode started"
    field_name = "start"
    display_name = "Start"
    widget = "search/widgets/date.html"


class EpisodeEnd(
    EpisodeDateQuery, SearchRuleField
):
    type = "date"
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
    type = "many_to_many"
    type_display_name = "Text Field"
    field_name = "team"
    widget = "search/widgets/many_to_many.html"

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
