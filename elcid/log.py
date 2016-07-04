import logging
import sys
import traceback
from django.utils.log import AdminEmailHandler


class MailFormatter(logging.Formatter):
    """ the message may contain sensitive patient information
        so just show the stack trace
    """
    def __init__(self, *args, **kwargs):
        super(MailFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        record.msg = 'censored'

        if record.exc_text:
            stack_trace = record.exc_text.split("\n")
            # shave the last line off the stack trace
            # in case it contains identifiable data
            record.exc_text = "\n".join(stack_trace[:-1])
        return super(MailFormatter, self).format(record)


class ConfidentialEmailer(AdminEmailHandler):
    def __init__(self, *args, **kwargs):
        super(ConfidentialEmailer, self).__init__(*args, **kwargs)
        self.include_html = False

    def format_subject(self, subject):
        return "elCID error"
