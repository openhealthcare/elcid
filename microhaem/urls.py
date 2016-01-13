"""
Root elCID urlconf
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from microhaem import views

urlpatterns = patterns(
    '',
    url(r'^patient/(?P<patient_id>\d+)', views.MicroHaemDataView.as_view(), name="microhaem_data_view"),
    url(r'^templates/patient_notes.html$', views.MicroHaemTemplateView.as_view(), name="microhaem_template_view"),
)
