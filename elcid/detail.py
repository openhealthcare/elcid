from opal.core import detail
from django.conf import settings


if settings.GLOSS_ENABLED:
    class Result(detail.PatientDetailView):
        display_name = "Test Results"
        order = 5
        template = "detail/result.html"
