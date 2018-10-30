"""
eLCID specific views.
"""
import csv
import random

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView, View

from opal.core import application

app = application.get_app()


def temp_password():
    num = random.randint(10, 99)
    word = random.choice(['womble', 'bananas', 'flabbergasted', 'kerfuffle'])
    return '{0}{1}'.format(num, word)


class Error500View(View):
    """
    Demonstrative 500 error to preview templates.
    """
    def get(self, *args, **kwargs):
        if self.request.META['HTTP_USER_AGENT'].find('Googlebot') != -1:
            return HttpResponse('No')
        raise Exception("This is a deliberate error")


class StoriesView(LoginRequiredMixin, TemplateView):
    template_name = "stories.html"
