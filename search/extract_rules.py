from opal.core import discoverable
from six import text_type
from opal import models
from opal.core import subrecords
from elcid import models as emodels
from search import subrecord_discoverable
from search.exceptions import SearchException


class CsvFieldWrapper(subrecord_discoverable.SubrecordFieldWrapper):
    description_template = "search/extract_rule_description.html"
    required = False

    def extract(self, obj):
        result = getattr(obj, self.field_name)
        if result is None:
            return ""
        return result

    def get_description_template(self):
        return self.description_template

    def to_dict(self):
        as_dict = super(CsvFieldWrapper, self).to_dict()
        as_dict["required"] = self.get_required()
        return as_dict

    def get_required(self):
        return self.required


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


class ExtractRule(
    subrecord_discoverable.SubrecordDiscoverableMixin,
    discoverable.DiscoverableFeature,
):
    module_name = 'extract_rule_description'

    def get_model_fields(self):
        if self.user.profile.roles.filter(
            name="extract_personal_details"
        ).exists():
            field_names = self.model._get_fieldnames_to_serialize()
        else:
            field_names = self.model._get_fieldnames_to_extract()

        if "consistency_token" in field_names:
            field_names.remove("consistency_token")
        if "id" in field_names:
            field_names.remove("id")
        if "episode_id" in field_names:
            field_names.remove("episode_id")
        if "patient_id" in field_names:
            field_names.remove("patient_id")
        return field_names

    def get_fields(self):
        fields = super(ExtractRule, self).get_fields()
        if self.model:
            if isinstance(self.model, models.PatientSubrecord):
                fields.insert(EpisodeIdForPatientSubrecord(), 0)

            if isinstance(self.model, models.EpisodeSubrecord):
                fields.insert(PatientIdForEpisodeSubrecord(), 0)
        return fields

    def get_renderer(self):
        from search import extract_renderers
        if self.model:
            if self.model in subrecords.patient_subrecords():
                return extract_renderers.PatientSubrecordCsvRenderer
            elif self.model in subrecords.episode_subrecords():
                return extract_renderers.EpisodeSubrecordCsvRenderer
        raise SearchException(
            "please implement get_renderer for {}".format(self)
        )

    def cast_field_name_to_attribute(self, str):
        return CsvFieldWrapper(self.user, self.model, str)


class EpisodeTeamExtractField(CsvFieldWrapper):
    display_name = "Team"
    description = "The team(s) related to an episode of care"
    type = "many_to_many"
    type_display_name = "Text Field"
    field_name = "Team"

    def extract(self, obj):
        return text_type(";".join(
            obj.get_tag_names(self.user, historic=True)
        ))


class EpisodeExtractRule(ExtractRule):
    fields = [
        EpisodeTeamExtractField,
        "start",
        "end",
        "created",
        "updated",
        "created_by_id",
        "updated_by_id",
    ]
    model = models.Episode
    display_name = "Episode"
    slug = "episode"
    lookup_list = []

    def get_renderer(self):
        from search import extract_renderers
        return extract_renderers.EpisodeCsvRenderer


class ResultSerializer(ExtractRule):
    exclude = True
    slug = emodels.Result.get_api_name()


class DemographicsSexField(CsvFieldWrapper):
    field_name = "sex"
    model = emodels.Demographics
    required = True


class DemographicsDateOfBirthField(CsvFieldWrapper):
    field_name = "date_of_birth"
    model = emodels.Demographics
    required = True


class DemographicsSerializer(ExtractRule):
    slug = emodels.Demographics.get_api_name()
    model = emodels.Demographics
    field_sex = DemographicsSexField
    field_date_of_birth = DemographicsDateOfBirthField


class MicroTestRule(ExtractRule):
    slug = emodels.MicrobiologyTest.get_api_name()
    model = emodels.MicrobiologyTest

    MICRO_FIELDS_TO_IGNORE = [
        "test",
        "date_ordered",
        "details",
        "microscopy",
        "organism",
        "sensitive_antibiotics",
        "resistant_antibiotics"
    ]

    def get_model_fields(self, *args, **kwargs):
        model_fields = super(MicroTestRule, self).get_model_fields(
            *args, **kwargs
        )
        return [
            f for f in model_fields if f not in self.MICRO_FIELDS_TO_IGNORE
        ]


class DuplicatePatientQuery(ExtractRule):
    exclude = True
    slug = emodels.DuplicatePatient.get_api_name()
