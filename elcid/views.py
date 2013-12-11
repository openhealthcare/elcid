"""
eLCID specific views.
"""
from django.views.generic import TemplateView, View
from letter.contrib.contact import EmailForm, EmailView

u = unicode

class FeedbackForm(EmailForm):
    """
    Form for our feedback submissions.
    """
    def body(self):
        return u"Feedback-form from: {0}\n\n{1}".format(
            u'{0} <{1}>'.format(
                u(self.cleaned_data.get('name', '')),
                u(self.cleaned_data.get('email', ''))),
            u(self.cleaned_data.get('message', '')))

    def subject(self): return u'eLCID - Feedback Form'
    def reply_to(self): return u(self.cleaned_data.get('email', ''))


class FeedbackView(EmailView):
    template_name = 'feedback.html'
    form_class    = FeedbackForm
    success_url   = '/feedback/sent'


class FeedbackSentView(TemplateView):
    template_name = 'feedback_sent.html'


class Error500View(View):
    """
    Demonstrative 500 error to preview templates.
    """
    def get(self, *args, **kwargs):
        raise Exception("This is a deliberate error")
