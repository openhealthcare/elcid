from opal.core.patient_lists import TaggedPatientList, PatientList
from elcid import models
from opal.models import Episode


class InfectionControl(TaggedPatientList):
    tag = "infectioncontrol"

    schema = [
        models.Demographics,
        models.Location,
        models.MicrobiologyTest,
    ]


class Mine(PatientList):
    """
    if the user has tagged episodes as their's this will give them the appropriate
    episode queryset
    """
    @classmethod
    def get(klass, **kwargs):
        tag = kwargs.get("tag", None)
        if tag and "mine" == tag.lower():
            return klass

    def get_queryset(self):
        return Episode.objects.filter(tagging__user=self.request.user)
