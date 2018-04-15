from six import text_type

from opal.core import discoverable
from opal import models
from elcid import models as emodels
from search.subrecord_discoverable import (
    SubrecordFieldWrapper, SubrecordDiscoverableMixin
)


class CsvFieldWrapper(SubrecordFieldWrapper):
    def extract(self, obj):
        return getattr(obj, self.field_name)


class EpisodeIdForPatientSubrecord(CsvFieldWrapper):
    display_name = "Episode"
    field_name = "episode_id"

    def extract(self, obj):
        return obj.episode.id


class PatientIdForEpisodeSubrecord(CsvFieldWrapper):
    display_name = "Patient"
    field_name = "patient_id"

    def extract(self, obj):
        return obj.patient.id


class CsvSerializer(
    SubrecordDiscoverableMixin,
    discoverable.DiscoverableFeature
):
    module_name = 'extract_serialisers'

    def get_model_fields(self):
        field_names = self.model._get_fieldnames_to_extract()
        if "consistency_token" in field_names:
            field_names.remove("consistency_token")
        if "id" in field_names:
            field_names.remove("id")
        return field_names

    def get_fields(self):
        fields = super(CsvSerializer, self).get_fields()
        if self.model:
            if isinstance(self.model, models.PatientSubrecord):
                fields.insert(EpisodeIdForPatientSubrecord(), 0)

            if isinstance(self.model, models.EpisodeSubrecord):
                fields.insert(PatientIdForEpisodeSubrecord(), 0)
        return fields

    def get_renderer(self):
        from search import extract_renderers
        if self.model:
            if isinstance(self.model, models.PatientSubrecord):
                return extract_renderers.PatientSubrecordCsvRenderer
            elif isinstance(self.model, models.EpisodeSubrecord):
                return extract_renderers.EpisodeSubrecordCsvRenderer
        return extract_renderers.CsvRenderer

    def cast_field_name_to_attribute(self, str):
        return CsvFieldWrapper(self.user, self.model, str)


class EpisodeTeamExtractField(CsvFieldWrapper):
    field_name = "team"
    display_name = "Team"
    description = "The team(s) related to an episode of care"

    @property
    def enum(self):
        return [i["title"] for i in models.Tagging.build_field_schema()]

    def extract(self, obj):
        return text_type(";".join(
            obj.get_tag_names(self.user, historic=True)
        ))


class EpisodeCsvSerializer(CsvSerializer):
    fields = [
        EpisodeTeamExtractField,
        "start",
        "end",
        "created",
        "updated",
        "created_by_id",
        "updated_by_id",
        "patient_id"
    ]
    model = models.Episode
    display_name = "Episode"
    slug = "episode"

    def get_renderer(self):
        from search import extract_renderers
        return extract_renderers.EpisodeCsvRenderer


class ResultQuery(CsvSerializer):
    exclude = True
    slug = emodels.Result.get_api_name()
