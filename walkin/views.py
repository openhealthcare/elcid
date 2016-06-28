"""
Views for the OPAL walkin plugin
"""
from django.views.generic import TemplateView

from opal.core.views import LoginRequiredMixin

class DischargeWalkinEpisodeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'discharge_walkin_episode.html'

    def get_context_data(self, **kwargs):
        from opal import models

        context = super(DischargeWalkinEpisodeTemplateView, self).get_context_data(**kwargs)
        context['teams'] = models.Team.for_user(self.request.user)
        return context
