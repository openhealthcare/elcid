"""
The custom Micro Haem detail view.
"""
from opal.core import detail
from opal.models import UserProfile

class MicroHaemPatientView(detail.PatientDetailView):
    order = 1
    name = 'micro_haem'
    title = 'Micro Haem'
    template   = 'detail/micro_haem.html'

    @classmethod
    def visible_to(self, user):
        return UserProfile.objects.filter(
            user=user,
            roles__name='micro_haem'
        ).count() > 0
