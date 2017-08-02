from opal.core.patient_lists import PatientList
from elcid import models
from opal.models import Episode
from opal.utils import AbstractBase

list_columns = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.Travel,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.GeneralNote,
    models.Todo,
]


class ElcidPatientList(PatientList, AbstractBase):
    comparator_service = "LocationWardComparator"


class Mine(ElcidPatientList):
    """
    if the user has tagged episodes as their's this will give them the appropriate
    episode queryset
    """
    display_name = 'Mine'
    order = 100
    schema = list_columns

    @classmethod
    def get(klass, **kwargs):
        tag = kwargs.get("tag", None)
        if tag and "mine" == tag.lower():
            return klass

    def get_queryset(self, *args, **kwargs):
        return Episode.objects.filter(tagging__value='mine')

    def to_dict(self, user):
        qs = self.get_queryset(user).filter(tagging__user=user)
        return qs.serialised_active(user)
