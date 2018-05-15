from elcid import models as emodels
from search.search_rules import SearchRule


class DuplicatePatientQuery(SearchRule):
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


class ResultQuery(SearchRule):
    exclude = True
    slug = emodels.Result.get_api_name()


class ContactDetailsSearchRule(SearchRule):
    slug = emodels.ContactDetails.get_api_name()
    display_name = "Patient Contact Details"
    model = emodels.ContactDetails
