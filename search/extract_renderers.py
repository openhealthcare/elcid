import logging
import csv

from collections import defaultdict
from six import text_type
from django.utils.functional import cached_property
from django.db.models import Count, Max
from django.utils.encoding import force_bytes

from search.exceptions import SearchException


def _encode_to_utf8(some_var):
    if not isinstance(some_var, text_type):
        return some_var
    else:
        return force_bytes(some_var)


class CsvRenderer(object):
    """
        An Abstract base class of the other csv renderers
    """

    # overrides of model fields for the csv columns
    non_field_csv_columns = []

    def __init__(self, serializer, queryset, user, chosen_fields_names=None):
        self.serializer = serializer
        self.queryset = queryset
        self.user = user
        self.chosen_fields_names = chosen_fields_names

    def get_fields(self):
        """
            If we've got fields declared, returned them.
        """
        if self.chosen_fields_names:
            return [
                self.serializer.get_field(i) for i in self.chosen_fields_names
            ]
        else:
            return self.serializer.get_fields()

    def get_field(self, field_name):
        for i in self.get_fields():
            if i.get_name() == field_name:
                return i
        raise SearchException("Unable to find field {} for {}".format(
            field_name, self.get_display_name()
        ))

    def exists(self):
        if self.serializer.model:
            if self.serializer.model._is_singleton:
                return self.queryset.exclude(updated=None).exists()

        if isinstance(self.queryset, list):
            return bool(self.queryset)

        return self.queryset.exists()

    def get_field_title(self, field_name):
        return self.serializer.get_field(field_name).get_display_name()

    def get_headers(self):
        result = []
        for field in self.get_fields():
            result.append(field.get_display_name())
        return result

    def get_field_value(self, field, obj):
        col_value = field.extract(obj)

        if isinstance(col_value, list):
            as_str = "; ".join(text_type(i) for i in col_value)
        else:
            as_str  = text_type(col_value)
        return _encode_to_utf8(as_str)

    def get_row(self, instance, *args, **kwargs):
        result = []
        for i in self.get_fields():
            result.append(self.get_field_value(i, instance))
        return result

    def get_rows(self):
        for instance in self.queryset:
            yield self.get_row(instance)

    def count(self):
        return self.queryset.count()

    @cached_property
    def flat_row_length(self):
        return len(self.get_flat_headers())

    def get_flat_headers(self):
        single_headers = self.get_headers()

        if self.flat_repetitions == 1:
            return [
                "{0} {1}".format(
                    self.serializer.get_display_name(),
                    i
                ) for i in single_headers
            ]

        result = []

        for rep in range(self.flat_repetitions):
            result.extend(
                (
                    "{0} {1} {2}".format(
                        self.serializer.get_display_name(),
                        rep + 1,
                        i
                    ) for i in single_headers
                )
            )
        return result


class PatientSubrecordCsvRenderer(CsvRenderer):
    def __init__(
        self, serializer, episode_queryset, user, chosen_fields_names=None
    ):
        self.patient_to_episode = defaultdict(list)

        for episode in episode_queryset:
            self.patient_to_episode[episode.patient_id].append(episode.id)

        queryset = serializer.model.objects.filter(
            patient__in=list(self.patient_to_episode.keys()))

        super(PatientSubrecordCsvRenderer, self).__init__(
            serializer, queryset, user, chosen_fields_names
        )

    def get_display_name(self):
        return self.serializer.get_display_name()

    def get_rows(self):
        for sub in self.queryset:
            for episode_id in self.patient_to_episode[sub.patient_id]:
                yield self.get_row(sub, episode_id)

    @cached_property
    def flat_repetitions(self):
        if not self.queryset.exists():
            return 1

        if self.serializer.model._is_singleton:
            return 1

        annotated = self.queryset.values('patient_id').annotate(
            Count('patient_id')
        )
        return annotated.aggregate(Max('patient_id__count'))[
            "patient_id__count__max"
        ]

    def get_nested_row(self, episode):
        nested_subrecords = self.queryset.filter(
            patient__episode=episode
        )
        result = []
        for nested_subrecord in nested_subrecords:
            result.extend(self.get_row(nested_subrecord, episode.id))

        while len(result) < self.flat_row_length:
            result.append('')
        return result


class EpisodeSubrecordCsvRenderer(CsvRenderer):
    def __init__(
        self, serializer, episode_queryset, user, chosen_fields_names=None
    ):

        queryset = serializer.model.objects.filter(
            episode__in=episode_queryset
        )

        super(EpisodeSubrecordCsvRenderer, self).__init__(
            serializer, queryset, user, chosen_fields_names
        )

    def get_display_name(self):
        return self.serializer.get_display_name()

    @cached_property
    def flat_repetitions(self):
        if not self.queryset:
            return 1

        if self.serializer.model._is_singleton:
            return 1

        annotated = self.queryset.values('episode_id').annotate(
            Count('episode_id')
        )
        return annotated.aggregate(Max('episode_id__count'))[
            "episode_id__count__max"
        ]

    def get_nested_row(self, episode):
        nested_subrecords = self.queryset.filter(episode=episode)
        result = []
        for nested_subrecord in nested_subrecords:
            result.extend(self.get_row(nested_subrecord))

        while len(result) < self.flat_row_length:
            result.append('')
        return result


class EpisodeCsvRenderer(CsvRenderer):
    def exists(self):
        # always have an episodes file
        return True

    def get_display_name(self):
        return self.model.get_display_name()

    def get_flat_headers(self):
        single_headers = super(
            EpisodeCsvRenderer, self
        ).get_headers()

        return ["Episode {}".format(i) for i in single_headers]

    def get_nested_row(self, episode):
        return super(EpisodeCsvRenderer, self).get_row(
            episode
        )
