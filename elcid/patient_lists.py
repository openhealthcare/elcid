from opal.core.patient_lists import PatientList
from elcid import models
from opal.models import Episode

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


class Mine(PatientList):
    """
    if the user has tagged episodes as their's this will give them the appropriate
    episode queryset
    """
    display_name = 'Mine'
    order = 100
    schema = list_columns
    allow_add_patient = False

    @classmethod
    def get(klass, **kwargs):
        tag = kwargs.get("tag", None)
        if tag and "mine" == tag.lower():
            return klass

    def get_queryset(self):
        return Episode.objects.filter(tagging__value='mine')

    def to_dict(self, user):
        qs = self.get_queryset().filter(tagging__user=user)
        return qs.serialised_active(user)
