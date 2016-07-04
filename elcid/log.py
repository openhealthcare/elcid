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

        return super(MailFormatter, self).format(record)


class ConfidentialEmailer(AdminEmailHandler):
    def __init__(self, *args, **kwargs):
        super(ConfidentialEmailer, self).__init__(*args, **kwargs)
        self.include_html = False

    def emit(self, record):
        subject = self.format_subject(self.format(record))
        message = ""

        if hasattr(sys, "last_traceback"):
            tb = traceback.extract_tb(sys.last_traceback)
            message = traceback.format_list(tb)[:-1]
            message = "\n".join(message)

        self.send_mail(subject, message, fail_silently=True, html_message=None)
