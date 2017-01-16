"""
Root elCID urlconf
"""
from django.conf.urls import patterns, url, include
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin

admin.autodiscover()

from opal.urls import urlpatterns as opatterns
from elcid import api

from elcid import views

urlpatterns = patterns(
    '',
    url(
        '^admin/bulk-create-users$',
        staff_member_required(views.BulkCreateUserView.as_view()),
        name='bulk-create-users'
    ),
    url(r'^test/500$', views.Error500View.as_view(), name='test-500'),
    url(r'^templates/elcid/modals/(?P<name>[a-z_]+.html)$', views.ElcidTemplateView.as_view()),
    url(r'stories/$', views.TemplateView.as_view(template_name='stories.html')),
    url(r'glossapi/v0.1/', include(api.router.urls)),
)

urlpatterns += opatterns
