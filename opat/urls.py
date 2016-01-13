"""
Urls for the opat OPAL plugin
"""
from django.conf.urls import patterns, url

from opat import views

urlpatterns = patterns(
    '',
    url(r'^opat/templates/modals/discharge_opat_episode.html/?$',
        views.DischargeOpatEpisodeTemplateView.as_view()),
    url(r'^opat/templates/modals/opat_referral.html/?$',
        views.OpatReferralTemplateView.as_view()),
    url(r'^opat/templates/modals/add_episode.html/?$',
        views.OpatAddEpisodeTemplateView.as_view()),
)
