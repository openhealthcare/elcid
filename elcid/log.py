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

        if record.exc_text:
            stack_trace = record.exc_text.split("\n")
            # shave the last line off the stack trace
            # in case it contains identifiable data
            record.exc_text = "\n".join(stack_trace[:-1])

        return super(ConfidentialEmailer, self).emit(record)
