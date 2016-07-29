"""
Views for the opat OPAL Plugin
"""
from django.views.generic import TemplateView
from opal.core.views import LoginRequiredMixin

class DischargeOpatEpisodeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'discharge_opat_episode_modal.html'


class OpatReferralTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'opat_referral_modal.html'


class OpatAddEpisodeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'opat/add_episode_modal.html'
