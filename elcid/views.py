"""
eLCID specific views.
"""
import csv
import random

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView, View

import letter
from letter.contrib.contact import EmailForm, EmailView

from opal.core.subrecords import subrecords
from opal.core.views import _build_json_response
from opal import models as opal_models
from opal.core import application

from elcid.forms import BulkCreateUsersForm

app = application.get_app()
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

    def subject(self):
        return u'eLCID - Feedback Form'

    def reply_to(self):
        return u(self.cleaned_data.get('email', ''))


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
        if self.request.META['HTTP_USER_AGENT'].find('Googlebot') != -1:
            return HttpResponse('No')
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

        return super(BulkCreateUserView, self).form_valid(form)


class PatientDetailDataView(View):
    """
    Return a serialised view of the patient.
    """
    def get(self, *args, **kwargs):
        patient_id = kwargs.get("patient_id")
        episode = get_object_or_404(opal_models.Episode, id=patient_id)

        serialised = opal_models.Episode.objects.serialised(
            self.request.user,
            [episode]
        )

        return _build_json_response(serialised)


class PatientDetailTemplateView(TemplateView):
    template_name = 'patient_notes.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PatientDetailTemplateView, self).get_context_data(*args, **kwargs)
        context['models'] = {m.__name__: m for m in subrecords()}
        context['inline_forms'] = getattr(app, "patient_view_forms", [])
        return context


class ElcidTemplateView(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.name = kwargs['name']
        return super(ElcidTemplateView, self).dispatch(*args, **kwargs)

    def get_template_names(self, *args, **kwargs):
        return ['elcid/modals/'+self.name]
