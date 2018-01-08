"""
Views for the OPAL walkin plugin
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from opal import models

class DischargeWalkinEpisodeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'discharge_walkin_episode.html'
