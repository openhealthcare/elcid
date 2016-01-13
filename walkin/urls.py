"""
Urls for the OPAL Walk In plugin
"""
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from walkin import views

urlpatterns = patterns(
    '',
    url('^templates/modals/discharge_walkin_episode.html/?$',
        views.DischargeWalkinEpisodeTemplateView.as_view()),
    url('^templates/modals/add_walkin_episode.html/?$',
        TemplateView.as_view(template_name='add_walkin_episode_modal.html')),
    url('^walkin/modals/nurse_investigations.html$',
        TemplateView.as_view(template_name='modals/nurse_investigations.html')),
)
