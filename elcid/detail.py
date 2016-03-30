from opal.core import detail


class Result(detail.PatientDetailView):
    display_name = "Test Results"
    order = 5
    template = "detail/result.html"
