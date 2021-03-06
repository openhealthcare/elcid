"""
Root elCID urlconf
"""
from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import admin

admin.autodiscover()

from opal.urls import urlpatterns as opatterns

from elcid import views

urlpatterns = [
    url(
        r'^referrals/?$', views.TemplateView.as_view(
            template_name='referral/referral_list.html'
        )
    ),
    url(r'^test/500$', views.Error500View.as_view(), name='test-500'),
    url(
        r'stories/$',
        views.StoriesView.as_view(),
        name='stories'
    ),
]

urlpatterns += opatterns
