from opal.core import detail
from django.conf import settings


class Result(detail.PatientDetailView):
    display_name = "Test Results"
    order = 5
    template = "detail/result.html"

    @classmethod
    def visible_to(klass, user):
        if user.is_superuser:
            return True
        return settings.GLOSS_ENABLED
