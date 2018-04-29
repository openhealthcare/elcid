import operator

from django.db.models import Q
from opal import models
from search.exceptions import SearchException
from django.contrib.contenttypes.models import ContentType


def model_name(model):
    return model.__name__.lower()


def query_episodes_by_kwargs(model, filter_kwargs):
    if issubclass(model, models.EpisodeSubrecord):
        return models.Episode.objects.filter(**filter_kwargs)
    elif issubclass(model, models.PatientSubrecord):
        pats = models.Patient.objects.filter(**filter_kwargs)
        return models.Episode.objects.filter(
            patient__in=pats
        )
    else:
        raise NotImplementedError(
            "please implement custom query types for non subrecords"
        )


def query_for_text_fields(model, field_name, value, query_type, ):
    contains = '__iexact'
    if query_type == 'Contains':
        contains = '__icontains'
    queryset_path = '{0}__{1}{2}'.format(
        model_name(model), field_name, contains
    )
    kw = {queryset_path: value}
    return query_episodes_by_kwargs(model, kw)


def query_for_date_fields(model, field_name, value, query_type):
    value = models.deserialize_date(value)
    if query_type not in {"Before", "After"}:
        raise SearchException(
            "Date queries required before or after to be declared"
        )
    if query_type == 'Before':
        qtype = '__lte'
    elif query_type == 'After':
        qtype = '__gte'

    kw = {
        '{0}__{1}{2}'.format(model_name(model), field_name, qtype): value
    }
    return query_episodes_by_kwargs(model, kw)


def query_for_number_fields(model, field_name, value, query_type):
    if query_type not in {"Greater Than", "Less Than"}:
        raise SearchException(
            "Number queries must be greater than or less than"
        )

    if query_type == 'Greater Than':
        qtype = '__gt'
    elif query_type == 'Less Than':
        qtype = '__lt'
    kw = {'{0}__{1}{2}'.format(
        model_name(model), field_name, qtype): value
    }
    return query_episodes_by_kwargs(model, kw)


def query_for_boolean_fields(model, field_name, value):
    if value not in {"true", "false"}:
        raise SearchException(
            "Boolean queries must be true or false"
        )

    val = value == 'true'
    kw = {'{0}__{1}'.format(model_name(model), field_name): val}
    return query_episodes_by_kwargs(model, kw)


def query_for_related_fields(model, field_namne, value, query_type):
    raise NotImplementedError("elect queries need to be implement")


def query_for_fkorft_fields(model, field_name, value, query_type):
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
    contains = '__iexact'
    if query_type == 'Contains':
        contains = '__icontains'

    related_query_name = model._meta.model_name
    if issubclass(model, models.EpisodeSubrecord):
        qs = models.Episode.objects.all()
    elif issubclass(model, models.PatientSubrecord):
        qs = models.Patient.objects.all()

    # 1)
    free_text_query = {
        '{0}__{1}_ft{2}'.format(
            related_query_name, field_name, contains
        ): value
    }

    # get all synonyms, if this is an 'Equal' query,
    # the return should be a list containing a single response.
    # Otherwise it's all of names of fields that have synonyms
    # that contain the query
    lookuplist_names = get_lookuplist_names_for_query_string(
        getattr(model, field_name).foreign_model,
        contains,
        value
    )

    # 2.1)
    foreign_key_query = {
        '{0}__{1}_fk__name{2}'.format(
            related_query_name,
            field_name,
            contains
        ): value
    }

    q_objects = [Q(**foreign_key_query), Q(**free_text_query)]

    # 2.2
    if query_type == "Contains":
        # add in those that have synonyms that contain the query
        # expression
        for name in lookuplist_names:
            keyword = "{0}__{1}_fk__name".format(
                related_query_name,
                field_name
            )
            q_objects.append(Q(**{keyword: name}))
    else:
        if lookuplist_names:
            synonym_equals = {
                '{0}__{1}_fk__name'.format(
                    related_query_name,
                    field_name
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


def get_lookuplist_names_for_query_string(
    lookuplist, contains, value
):
    """
    Returns a list of canonical terms from a given LOOKUPLIST that match
    QUERY_STRING respecting CONTAINS - which will be one of:
    '__iexact'
    '__icontains'
    """
    from opal.models import Synonym
    content_type = ContentType.objects.get_for_model(lookuplist)
    filter_key_words = dict(content_type=content_type)
    filter_key_words["name{0}".format(contains)] = value
    synonyms = Synonym.objects.filter(**filter_key_words)
    return [synonym.content_object.name for synonym in synonyms]


def query_for_many_to_many_fields(model, field_name, value, query_type):
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
    related_query_name = model._meta.model_name

    if issubclass(model, models.EpisodeSubrecord):
        qs = models.Episode.objects.all()
    elif issubclass(model, models.PatientSubrecord):
        qs = models.Patient.objects.all()

    contains = '__iexact'
    if query_type == 'Contains':
        contains = '__icontains'

    lookuplist = getattr(model, field_name).rel.model

    lookuplist_names = get_lookuplist_names_for_query_string(
        lookuplist, contains, value
    )

    # 1)
    non_synonym_query = {
        '{0}__{1}__name{2}'.format(
            related_query_name, field_name, contains
        ): value
    }

    q_objects = [Q(**non_synonym_query)]

    # 2)
    if query_type == "Contains":
        # add in those that have synonyms that contain the query
        # expression
        for name in lookuplist_names:
            keyword = "{0}__{1}__name".format(
                related_query_name, field_name
            )
            q_objects.append(Q(**{keyword: name}))
    else:
        if lookuplist_names:
            synonym_equals = {
                '{0}__{1}__name'.format(
                    related_query_name, field_name
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
