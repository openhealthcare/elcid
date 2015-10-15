"""
Root elCID urlconf
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from opal.urls import urlpatterns as opatterns

from elcid import views

urlpatterns = patterns(
    '',
    url('^admin/bulk-create-users$', views.BulkCreateUserView.as_view(), name='bulk-create-users'),
    url(r'^feedback/?$', views.FeedbackView.as_view(), name='feedback'),
    url(r'^feedback/sent/??$', views.FeedbackSentView.as_view(), name='feedback-sent'),
    url(r'^test/500$', views.Error500View.as_view(), name='test-500'),
    url(r'^templates/elcid/modals/(?P<name>[a-z_]+.html)$', views.ElcidTemplateView.as_view()),
    url(r'^patient/(?P<patient_id>\d+)', views.PatientDetailDataView.as_view(), name="patient_detail_data_view"),
    url(r'^templates/patient_notes.html$', views.PatientDetailTemplateView.as_view(), name="patient_detail_template_view"),
)

urlpatterns += opatterns
