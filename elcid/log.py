from django.utils.log import AdminEmailHandler


class ConfidentialEmailer(AdminEmailHandler):
    def __init__(self, *args, **kwargs):
        super(ConfidentialEmailer, self).__init__(*args, **kwargs)
        self.include_html = False

    def format_subject(self, subject):
        return "elCID error"

    def emit(self, record):
        record.msg = 'censored'
        record.args = []
        detail = ""
        if hasattr(record, "request"):
            detail = "{0} {1}".format(
                record.request.META.get("HTTP_HOST"),
                record.request.META.get("REQUEST_METHOD"),
            )
        record.request = None

        record.exc_text = "from {0}:{1}".format(
            record.filename,
            record.lineno
        )

        record.exc_text += "\n{}".format(detail)
        return super(ConfidentialEmailer, self).emit(record)
