import itertools
from opal.core import fields
from opal.core.discoverable import DiscoverableFeature
from opal import models
from elcid import models as emodels
from search.subrecord_discoverable import SubrecordDiscoverableMixin
from search import search_rule_fields
from search.exceptions import SearchException


"""
    A Search Rule a
    A Search Rule is roughly similar to a rest framework serialiser
    with bits...

    What we want is a discoverable that will return a search rule if its
    set or a model wrapped in a search field if its not.

    Similar to a Step in a pathway.

    Fields are declared on the search rule or default to all.

    A search rule field takes in a query, and is serialised to an extract.

    stage 1.
    Just do the wrap.

    stage 2.
    Manage the serialisation.
"""


class SearchRule(
    SubrecordDiscoverableMixin, DiscoverableFeature
):
    module_name = "search_rules"
    FIELDS_TO_IGNORE = {
        "id",
        "created",
        "updated",
        "created_by_id",
        "updated_by_id",
        "consistency_token",
        "episode_id",
        "patient_id"
    }

    def cast_field_name_to_attribute(self, str):
        if isinstance(
            getattr(self.model, str), fields.ForeignKeyOrFreeText
        ):
            field = getattr(self.model, str)
        else:
            field = self.model._meta.get_field(str)

        field_mapping = search_rule_fields.FIELD_TYPE_TO_SEARCH_RULE_FIELD

        for find_field_type, search_rule_field_cls in field_mapping.items():
            if find_field_type(field):
                return search_rule_field_cls(self.model, str)

        raise SearchException(
            "unable to find a field type for {} {}".format(
                self.model, str
            )
        )

    def get_description(self):
        return getattr(self, "description", "")

    def get_model_fields(self):
        result = self.model._get_fieldnames_to_serialize()
        result = [i for i in result if i not in self.FIELDS_TO_IGNORE]
        if issubclass(self.model, models.PatientSubrecord):
            result = [i for i in result if not i == "patient"]

        if issubclass(self.model, models.EpisodeSubrecord):
            result = [i for i in result if not i == "episode"]
        return result

    def query(self, given_query):
        given_field = given_query['field']
        query_field = self.get_field(given_field)
        return query_field.query(given_query)

    def get_widgets(self):
        for i in self.get_fields():
            yield i.get_widget()

    def get_widget_descriptions(self):
        for i in self.get_fields():
            yield i.get_widget_description()

    def get_query_description(self, given_query):
        """ This is the description used by in the downloaded query.txt
        """
        field = self.get_field(given_query["field"])
        return "{} {}".format(
            self.get_display_name(), field.get_query_description(given_query)
        )

    @classmethod
    def widgets(cls, user):
        all_widgets = (i.get_widgets() for i in cls.list_rules(user))
        return {i for i in itertools.chain(
            *all_widgets
        )}

    @classmethod
    def widget_descriptions(cls, user):
        widget_descriptions = (
            i.get_widget_descriptions() for i in cls.list_rules(user)
        )
        return {i for i in itertools.chain(
            *widget_descriptions
        )}


class AbstractLocationMixin(object):
    model = emodels.Location
    slug = emodels.Location.get_api_name()

    def sort_fields(self, fields):
        interested = [
            "hospital", "ward", "bed"
        ]
        name_to_field = dict()
        result = []
        for field in fields:
            if field.get_name() in interested:
                name_to_field[field.get_name()] = field
            else:
                result.append(field)

        for field_name in interested:
            result.insert(
                0, name_to_field[field_name]
            )
        return result


class EpisodeSearchRule(SearchRule):
    order = 1
    display_name = "Episode"
    slug = "episode"
    model = models.Episode
    fields = (
        search_rule_fields.EpisodeTeam,
        search_rule_fields.EpisodeCategory,
        search_rule_fields.EpisodeStart,
        search_rule_fields.EpisodeEnd
    )


class DemographicsExtractRule(SearchRule):
    order = 2
    slug = emodels.Demographics.get_api_name()
    model = emodels.Demographics


class DuplicatePatienSearchRule(SearchRule):
    exclude = True
    slug = emodels.DuplicatePatient.get_api_name()


class MicroTestRule(SearchRule):
    slug = emodels.MicrobiologyTest.get_api_name()
    model = emodels.MicrobiologyTest

    fields = [
        "test",
        "date_ordered",
        "details",
        "microscopy",
        "organism",
        "sensitive_antibiotics",
        "resistant_antibiotics"
    ]


class LocationRule(AbstractLocationMixin, SearchRule):
    pass


class ResultSearchRule(SearchRule):
    exclude = True
    slug = emodels.Result.get_api_name()


class CarersSearchRule(SearchRule):
    exclude = True
    slug = emodels.Carers.get_api_name()


class ContactDetailsSearchRule(SearchRule):
    slug = emodels.ContactDetails.get_api_name()
    model = emodels.ContactDetails
    exclude = True


class InpatientAdmissionSearchRule(SearchRule):
    slug = models.InpatientAdmission.get_api_name()
    model = models.InpatientAdmission
    exclude = True


class AppointmentSearchRule(SearchRule):
    slug = emodels.Appointment.get_api_name()
    model = emodels.Appointment
    exclude = True
