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
        subject = "elcid Error"
        message = "%s\n\nRequest repr(): %s" % (self.format(record), request_repr)
        self.send_mail(
            subject, message, fail_silently=True, html_message=None
        )
