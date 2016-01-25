from opal.core.patient_lists import TaggedPatientList, PatientList
from elcid import models
from opal.models import Episode


class Mine(PatientList):
    """
    if the user has tagged episodes as their's this will give them the appropriate
    episode queryset
    """
    order = 1
    url = "/#/list/mine"
    title = "Mine"

    @classmethod
    def get(klass, *args, **kwargs):
        tag = kwargs.get("tag", None)
        if tag and "mine" == tag.lower():
            return klass

    def get_queryset(self):
        return Episode.objects.filter(tagging__user=self.request.user)
