import logging
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

    def format_subject(self, subject):
        return "elCID error"
