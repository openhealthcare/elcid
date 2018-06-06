from six import text_type
from opal.core import discoverable
from opal import models
from opal.core import subrecords
from opal.core import fields
from elcid import models as emodels
from search import subrecord_discoverable
from search.exceptions import SearchException
from search import constants
from search import search_rules


class CsvFieldWrapper(subrecord_discoverable.SubrecordFieldWrapper):
    description_template = None
    required = False

    def extract(self, obj):
        result = getattr(obj, self.field_name)
        if result is None:
            return ""
        return result

    def to_dict(self):
        as_dict = super(CsvFieldWrapper, self).to_dict()
        as_dict["required"] = self.get_required()
        return as_dict

    def get_required(self):
        return self.required

    def get_description_template(self):
        if self.description_template:
            return self.description_template

        if self.field and subrecord_discoverable.is_boolean(self.field):
            return "search/field_descriptions/boolean.html"

        if self.field and subrecord_discoverable.is_date_time_field(
            self.field
        ):
            return "search/field_descriptions/date_time.html"

        if self.field and subrecord_discoverable.is_text(
            self.field
        ):
            return "search/field_descriptions/text.html"

        if self.field and fields.is_numeric(
            self.field
        ):
            return "search/field_descriptions/number.html"

        if self.field and subrecord_discoverable.is_date_field(self.field):
            return "search/field_descriptions/date.html"

        if self.field and subrecord_discoverable.is_text(self.field):
            return "search/field_descriptions/text.html"

        return "search/field_descriptions/generic.html"


class PatientIdForEpisodeSubrecord(CsvFieldWrapper):
    display_name = "Patient"
    field_name = "patient_id"
    type_display_name = "Patient Id"
    icon = False
    enum = False
    lookup_list = False
    description = "The ID of the Patient"

    def extract(self, obj):
        return obj.episode.patient.id


class UpdatedByField(CsvFieldWrapper):
    display_name = "Updated By"
    field_name = "updated_by_id"

    def extract(self, obj):
        if obj.updated_by:
            return obj.updated_by.username
        return ""

    def get_description_template(self):
        return "search/field_descriptions/changed_by.html"


class CreatedByField(CsvFieldWrapper):
    display_name = "Created By"
    field_name = "created_by_id"

    def extract(self, obj):
        if obj.created_by:
            return obj.created_by.username
        return ""

    def get_description_template(self):
        return "search/field_descriptions/changed_by.html"


class ExtractRule(
    subrecord_discoverable.SubrecordDiscoverableMixin,
    discoverable.DiscoverableFeature,
):
    module_name = 'extract_rules'

    FIELDS_TO_IGNORE = {
        "id",
        "created",
        "updated",
        "created_by_id",
        "updated_by_id",
        "consistency_token",
    }

    def get_model_fields(self):
        if self.user.profile.roles.filter(
            name=constants.EXTRACT_PERSONAL_DETAILS
        ).exists():
            field_names = self.model._get_fieldnames_to_serialize()
        else:
            field_names = self.model._get_fieldnames_to_extract()

        field_names = [
            i for i in field_names if i not in self.FIELDS_TO_IGNORE
        ]

        return field_names

    def get_fields(self):
        fields = super(ExtractRule, self).get_fields()
        if self.model:
            result = []

            # episode subrecords should include the patient id
            if self.model in subrecords.episode_subrecords():
                fields.append(PatientIdForEpisodeSubrecord(
                    self.user, model=self.model
                ))

            # episode id should appear first (or after patient id)
            patient_id = None
            episode_id = None
            for field in fields:
                field_name = field.get_name()
                if field_name == "episode_id":
                    episode_id = field
                elif field_name == "patient_id":
                    patient_id = field
                else:
                    result.append(field)

            if episode_id:
                result.insert(
                    0, episode_id
                )

            if patient_id:
                result.insert(
                    0, patient_id
                )

        return result

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

    def get_fields_for_schema(self):
        """ Whether this field should appear in the schema
        """
        fields = super(ExtractRule, self).get_fields_for_schema()
        to_exclude = {"episode_id", "patient_id"}
        return (i for i in fields if i.get_name() not in to_exclude)

    def cast_field_name_to_attribute(self, str):
        if str == "created_by_id":
            return CreatedByField(self.user, self.model, str)
        elif str == "updated_by_id":
            return UpdatedByField(self.user, self.model, str)
        return CsvFieldWrapper(self.user, self.model, str)


class EpisodeTeamExtractField(CsvFieldWrapper):
    display_name = "Team"
    description = "The team(s) related to an episode of care"
    type = "many_to_many"
    type_display_name = "Text Field"
    field_name = "team"
    description_template = "search/field_descriptions/episode/team.html"

    def extract(self, obj):
        return text_type(";".join(
            obj.get_tag_names(self.user, historic=True)
        ))


class EpisodeStartExtractField(CsvFieldWrapper):
    field_name = "start"
    description_template = "search/field_descriptions/date.html"
    model = models.Episode


class EpisodeEndExtractField(CsvFieldWrapper):
    field_name = "end"
    description_template = "search/field_descriptions/date.html"
    model = models.Episode


class EpisodePatientExtractField(CsvFieldWrapper):
    model = models.Episode
    field_name = "patient_id"
    display_name = "Patient ID"


class EpisodeExtractRule(ExtractRule):
    order = 1
    fields = [
        EpisodePatientExtractField,
        "id",
        EpisodeTeamExtractField,
        EpisodeStartExtractField,
        EpisodeEndExtractField,
    ]
    model = models.Episode
    display_name = "Episode"
    slug = "episode"
    lookup_list = []

    def get_renderer(self):
        from search import extract_renderers
        return extract_renderers.EpisodeCsvRenderer

    def get_fields_for_schema(self):
        """ Whether this field should appear in the schema
        """
        fields = super(ExtractRule, self).get_fields_for_schema()
        to_exclude = {"id", "patient_id"}
        return (i for i in fields if i.get_name() not in to_exclude)


class ResultSerializer(ExtractRule):
    exclude = True
    slug = emodels.Result.get_api_name()


class LocationRule(search_rules.AbstractLocationMixin, ExtractRule):
    pass


class DemographicsSexField(CsvFieldWrapper):
    field_name = "sex"
    model = emodels.Demographics
    required = True


class DemographicsDateOfBirthField(CsvFieldWrapper):
    field_name = "date_of_birth"
    model = emodels.Demographics
    required = True


class DemographicsExtractRule(ExtractRule):
    order = 2
    slug = emodels.Demographics.get_api_name()
    model = emodels.Demographics
    field_sex = DemographicsSexField
    field_date_of_birth = DemographicsDateOfBirthField


class DuplicatePatientQuery(ExtractRule):
    exclude = True
    slug = emodels.DuplicatePatient.get_api_name()
