from opal.core.patient_lists import TaggedPatientList, PatientList
from elcid import models
from opal.models import Episode


class Mine(PatientList):
    """
    if the user has tagged episodes as their's this will give them the appropriate
    episode queryset
    """
    display_name = 'Mine'
    order = 100

    @classmethod
    def get(klass, **kwargs):
        tag = kwargs.get("tag", None)
        if tag and "mine" == tag.lower():
            return klass

    def get_queryset(self):
        return Episode.objects.filter(tagging__value='mine')

    def to_dict(self, user):
        return self.get_queryset().filter(tagging__user=user).serialised_active(user)
