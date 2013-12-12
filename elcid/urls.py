from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
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
)

urlpatterns += opatterns
