"""
eLCID specific views.
"""
import csv
import random

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import TemplateView, FormView, View
import letter
from letter.contrib.contact import EmailForm, EmailView

from elcid.forms import BulkCreateUsersForm

u = unicode
POSTIE = letter.DjangoPostman()

def temp_password():
    num = random.randint(1, 100)
    word = random.choice(['womble', 'bananas', 'flabbergasted', 'kerfuffle'])
    return '{0}{1}'.format(num, word)

class FeedbackForm(EmailForm):
    """
    Form for our feedback submissions.
    """
    email = forms.EmailField(required=False)

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


class BulkCreateUserView(FormView):
    """
    Used in the admin - bulk create users.
    """
    form_class = BulkCreateUsersForm
    template_name = 'admin/bulk_create_users.html'
    success_url = '/admin/auth/user/'

    def form_valid(self, form):
        """
        Create the users from our uploaded file!

        Arguments:
        - `form`: Form

        Return: HTTPResponse
        Exceptions: None
        """
        usernames = [u.username for u in User.objects.all()]
        new_users = []

        for row in csv.reader(form.cleaned_data['users']):
            email = row[0]
            name_part, _ = email.split('@')

            # Check for reused usernames
            if name_part in usernames:
                form._errors['users'] = form.error_class(['Some of those users already exist :('])
                del form.cleaned_data['users']
                return self.form_invalid(form)

            frist, last = name_part.split('.')
            user = User(username=name_part,
                        email=email,
                        first_name=frist,
                        last_name=last,
                        is_active=True,
                        is_staff=False,
                        is_superuser=False)
            user.tp = temp_password()
            user.set_password(user.tp)
            new_users.append(user)

        for u in new_users:
            u.save()

            class Message(letter.Letter):
                Postie   = POSTIE

                From     = settings.DEFAULT_FROM_EMAIL
                To       = u.email
                Subject  = 'Your new account on eLCID'
                Template = 'email/new_user'
                Context  = {
                    'user': u
                    }

            Message.send()

        for u in new_users:
            print u, u.tp

        return super(BulkCreateUserView, self).form_valid(form)
