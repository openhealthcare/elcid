import logging
import csv

from collections import defaultdict
from six import text_type
from django.utils.functional import cached_property
from django.db.models import Count, Max
from django.utils.encoding import force_bytes

from search.exceptions import SearchException
from search import schemas


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

    def __init__(self, serialiser, queryset, user, chosen_fields_names=None):
        self.queryset = queryset
        self.user = user
        self.serialiser = serialiser
        self.chosen_fields_names = chosen_fields_names

    def get_fields(self):
        """
            If we've got fields declared, returned them.
        """
        if self.chosen_fields_names:
            return [
                self.serialiser.get_field(i) for i in self.chosen_fields_names
            ]
        else:
            return self.serialiser.get_fields()

    def get_field(self, field_name):
        for i in self.get_fields():
            if i.get_slug() == field_name:
                return i
        raise SearchException("Unable to find field {} for {}".format(
            field_name, self.get_display_name()
        ))

    def exists(self):
        if isinstance(self.queryset, list):
            return bool(self.queryset)
        return self.queryset.exists()

    def get_field_title(self, field_name):
        return self.serialiser.get_field(field_name).get_display_name()

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

    def write_to_file(self, file_name):
        logging.info("writing for {}".format(
            self.serialiser.get_display_name())
        )

        with open(file_name, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.get_headers())
            for row in self.get_rows():
                writer.writerow([i for i in row])

        logging.info("finished writing for {}".format(
            self.serialiser.get_display_name())
        )

    @cached_property
    def flat_row_length(self):
        return len(self.get_flat_headers())

    def get_flat_headers(self):
        single_headers = self.get_headers()

        if self.flat_repetitions == 1:
            return [
                "{0} {1}".format(
                    self.serialiser.get_display_name(),
                    i
                ) for i in single_headers
            ]

        result = []

        for rep in range(self.flat_repetitions):
            result.extend(
                (
                    "{0} {1} {2}".format(
                        self.serialiser.get_display_name(),
                        rep + 1,
                        i
                    ) for i in single_headers
                )
            )
        return result

    @classmethod
    def get_schema(cls, some_model):
        return schemas.extract_download_schema_for_model(some_model)


class PatientSubrecordCsvRenderer(CsvRenderer):
    def __init__(self, serialiser, episode_queryset, user, fields=None):
        self.patient_to_episode = defaultdict(list)

        for episode in episode_queryset:
            self.patient_to_episode[episode.patient_id].append(episode.id)

        queryset = serialiser.model.objects.filter(
            patient__in=list(self.patient_to_episode.keys()))

        super(PatientSubrecordCsvRenderer, self).__init__(
            serialiser.model, queryset, user, fields
        )

    def get_display_name(self):
        return self.serialiser.get_display_name()

    def get_rows(self):
        for sub in self.queryset:
            for episode_id in self.patient_to_episode[sub.patient_id]:
                yield self.get_row(sub, episode_id)

    @cached_property
    def flat_repetitions(self):
        if not self.queryset.exists():
            return 0

        if self.serialiser.model._is_singleton:
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
    def __init__(self, model, episode_queryset, user, fields=None):
        queryset = model.objects.filter(episode__in=episode_queryset)

        super(EpisodeSubrecordCsvRenderer, self).__init__(
            model, queryset, user, fields
        )

    def get_display_name(self):
        return self.serialiser.get_display_name()

    @cached_property
    def flat_repetitions(self):
        if not self.queryset:
            return 0

        if self.serialiser.model._is_singleton:
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
