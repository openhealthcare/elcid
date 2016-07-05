import logging
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
        record.request = None

        if record.exc_text:
            record.exc_text = "status code {0} from {1}:{2}".format(
                record.status_code,
                record.filename,
                record.lineno
            )

        return super(ConfidentialEmailer, self).emit(record)
