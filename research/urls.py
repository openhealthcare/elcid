"""
Urls for the OPAL Research plugin
"""
from django.conf.urls import patterns, url

from research import views

urlpatterns = patterns(
    '',
    url(r'^research/templates/(?P<name>[a-z_]+.html)$',
        views.ResearchTemplateView.as_view()),
)
