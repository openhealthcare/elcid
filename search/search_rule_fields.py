import datetime
import operator
from django.db import models as djangomodels
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from opal.core import fields
from opal.utils import camelcase_to_underscore
from opal import models
from search.exceptions import SearchException

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

    def query(self, query):
        querytype = query['queryType']
        contains = '__iexact'
        if querytype == 'Contains':
            contains = '__icontains'

        if isinstance(self.field, fields.ForeignKeyOrFreeText):
            return self._episodes_for_fkorft_fields(
                query, contains
            )

        if isinstance(self.field, djangomodels.BooleanField):
            return self._episodes_for_boolean_fields(
                query, contains
            )
        elif isinstance(self.field, djangomodels.DateField):
            return self._episodes_for_date_fields(
                query, contains
            )
        elif fields.is_numeric(self.field):
            return self._episodes_for_number_fields(
                query, contains
            )
        elif isinstance(self.field, djangomodels.ManyToManyField):
            return self._episodes_for_fkft_many_to_many_fields(
                query, contains
            )
        elif isinstance(
            self.field, (djangomodels.CharField, djangomodels.TextField,)
        ):
            queryset_path = '{0}__{1}{2}'.format(
                self.model_name, self.field_name, contains
            )
            kw = {queryset_path: query['query']}
            return self._episodes_for_filter_kwargs(kw, self.model)
        else:
            raise NotImplementedError("we do not support this")

    def _episodes_for_filter_kwargs(self, filter_kwargs, model):
        """
        For a given MODEL, return the Episodes that match for FILTER_KWARGS,
        understanding how to handle both EpispdeSubrecord and PatientSubrecord
        appropriately.
        """
        if issubclass(model, models.EpisodeSubrecord):
            return models.Episode.objects.filter(**filter_kwargs)
        elif issubclass(model, models.PatientSubrecord):
            pats = models.Patient.objects.filter(**filter_kwargs)
            return models.Episode.objects.filter(
                patient__in=pats
            )

    def _episodes_for_boolean_fields(self, query, contains):
        val = query['query'] == 'true'
        kw = {'{0}__{1}'.format(self.model_name, self.field_name): val}
        return self._episodes_for_filter_kwargs(kw, self.model)

    def _episodes_for_number_fields(self, query, contains):
        if query['queryType'] == 'Greater Than':
            qtype = '__gt'
        elif query['queryType'] == 'Less Than':
            qtype = '__lt'
        kw = {'{0}__{1}{2}'.format(
            self.model_name, self.field_name, qtype): query['query']
        }
        return self._episodes_for_filter_kwargs(kw, self.model)

    def _episodes_for_date_fields(self, query, contains):
        qtype = ''
        val = datetime.datetime.strptime(query['query'], "%d/%m/%Y")
        if query['queryType'] == 'Before':
            qtype = '__lte'
        elif query['queryType'] == 'After':
            qtype = '__gte'

        kw = {
            '{0}__{1}{2}'.format(self.model_name, self.field_name, qtype): val
        }
        return self._episodes_for_filter_kwargs(kw, self.model)

    def _episodes_for_fkorft_fields(self, query, contains):
        """
        Returns episodes that match QUERY.

        We are dealing with the Opal FreeTextOrForeignKey field.

        We need to construct a database query that will match episodes where:

        1) The free text value matches the query string
        2) The name of the foreign key value matches the query string
          - 2.1) This may be the canonical form (the .name attribute)
          - 2.2) This may be a synonymous form (a Synonym with a content_type)
                 that matches FIELD.foreign_model
        """
        related_query_name = self.model._meta.model_name
        if issubclass(self.model, models.EpisodeSubrecord):
            qs = models.Episode.objects.all()
        elif issubclass(self.model, models.PatientSubrecord):
            qs = models.Patient.objects.all()

        # 1)
        free_text_query = {
            '{0}__{1}_ft{2}'.format(
                related_query_name, self.field_name, contains
            ): query['query']
        }

        # get all synonyms, if this is an 'Equal' query,
        # the return should be a list containing a single response.
        # Otherwise it's all of names of fields that have synonyms
        # that contain the query
        lookuplist_names = self._get_lookuplist_names_for_query_string(
            getattr(self.model, self.field_name).foreign_model,
            query['query'],
            contains
        )

        # 2.1)
        foreign_key_query = {
            '{0}__{1}_fk__name{2}'.format(
                related_query_name,
                self.field_name,
                contains
            ): query['query']
        }

        q_objects = [Q(**foreign_key_query), Q(**free_text_query)]

        # 2.2
        if query["queryType"] == "Contains":
            # add in those that have synonyms that contain the query
            # expression
            for name in lookuplist_names:
                keyword = "{0}__{1}_fk__name".format(
                    related_query_name,
                    self.field_name
                )
                q_objects.append(Q(**{keyword: name}))
        else:
            if lookuplist_names:
                synonym_equals = {
                    '{0}__{1}_fk__name'.format(
                        related_query_name,
                        self.field_name
                        # Only one lookuplist entry can have matched because
                        # we're after an exact match on the query string rather
                        # than looking for all matches inside synonym names so
                        # we just take the [0]
                    ): lookuplist_names[0]
                }
                q_objects.append(Q(**synonym_equals))

        qs = qs.filter(reduce(operator.or_, q_objects)).distinct()

        if qs.model == models.Episode:
            return qs
        else:
            # otherwise its a patient
            return models.Episode.objects.filter(patient__in=qs).distinct()

    def _get_lookuplist_names_for_query_string(
            self, lookuplist, query_string, contains):
        """
        Returns a list of canonical terms from a given LOOKUPLIST that match
        QUERY_STRING respecting CONTAINS - which will be one of:
        '__iexact'
        '__icontains'
        """
        from opal.models import Synonym
        content_type = ContentType.objects.get_for_model(lookuplist)
        filter_key_words = dict(content_type=content_type)
        filter_key_words["name{0}".format(contains)] = query_string
        synonyms = Synonym.objects.filter(**filter_key_words)
        return [synonym.content_object.name for synonym in synonyms]

    def _episodes_for_fkft_many_to_many_fields(
        self, query, contains
    ):
        """
        Returns episodes that match QUERY.

        We are dealing with Django ManyToMany fields that link a subrecord
        to an Opal Lookuplist.

        We need to construct a database query that will match episodes where:

        1) The .name attribute of the FK target matches the query string
        2) A synonym of the FK target matches the query string
        """
        # looks for subrecords with many to many relations to the
        # fk or ft fields.
        related_query_name = self.model._meta.model_name

        if issubclass(self.model, models.EpisodeSubrecord):
            qs = models.Episode.objects.all()
        elif issubclass(self.model, models.PatientSubrecord):
            qs = models.Patient.objects.all()

        lookuplist = self.field.related_model
        lookuplist_names = self._get_lookuplist_names_for_query_string(
            lookuplist, query['query'], contains
        )

        # 1)
        non_synonym_query = {
            '{0}__{1}__name{2}'.format(
                related_query_name, self.field_name, contains
            ): query['query']
        }

        q_objects = [Q(**non_synonym_query)]

        # 2)
        if query["queryType"] == "Contains":
            # add in those that have synonyms that contain the query
            # expression
            for name in lookuplist_names:
                keyword = "{0}__{1}__name".format(
                    related_query_name, self.field_name
                )
                q_objects.append(Q(**{keyword: name}))
        else:
            if lookuplist_names:
                synonym_equals = {
                    '{0}__{1}__name'.format(
                        related_query_name, self.field_name
                    ): lookuplist_names[0]
                    # Only one lookuplist entry can have matched because
                    # we're after an exact match on the query string rather
                    # than looking for all matches inside synonym names so
                    # we just take the [0]
                }
                q_objects.append(Q(**synonym_equals))

        qs = qs.filter(reduce(operator.or_, q_objects)).distinct()

        if qs.model == models.Episode:
            return qs
        else:
            # otherwise its a patient
            return models.Episode.objects.filter(patient__in=qs).distinct()


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
