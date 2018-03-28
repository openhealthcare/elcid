"""
Urls for the elCID Research plugin
"""
from django.conf.urls import url

from research import views

urlpatterns = [
    url(r'^research/templates/(?P<name>[a-z_]+.html)$',
        views.ResearchTemplateView.as_view()),
]
