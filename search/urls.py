"""
Urls for Opal's search functionality
"""
from django.conf.urls import url

from search import views, api

urlpatterns = [
    url(r'^search/$', views.SearchIndexView.as_view(), name="search_index"),
    url(r'^search/templates/search.html/?$',
        views.SearchTemplateView.as_view()),

    url(r'^search/templates/extract.html/?$',
        views.ExtractTemplateView.as_view()),

    url(r'^search/templates/modals/save_filter_modal.html/?$',
        views.SaveFilterModalView.as_view()),

    url(r'^search/patient/?$',
        views.patient_search_view, name="patient_search"),

    url(r'^search/simple/$',
        views.simple_search_view, name="simple_search"),

    url(r'^search/extract/$',
        views.ExtractSearchView.as_view(), name="extract_search"),

    url(r'^search/extract/download$',
        views.DownloadSearchView.as_view(), name="extract_download"),

    url(r'^search/extract/status/(?P<task_id>[a-zA-Z0-9-]*)',
        views.ExtractStatusView.as_view(), name='extract_status'),

    url(r'^search/extract/download/(?P<task_id>[a-zA-Z0-9-]*)',
        views.ExtractFileView.as_view(), name='extract_file'),

    url(r'^search/extract/descriptions/slice/(?P<rule_api_name>[a-zA-Z0-9-_]*)/(?P<field_api_name>[a-zA-Z0-9-_]*)',
        views.ExtractSliceDescriptionView.as_view(), name='extract_slice_description'),
    url(r'^search/extract/descriptions/query/(?P<rule_api_name>[a-zA-Z0-9-_]*)/(?P<field_api_name>[a-zA-Z0-9-_]*)',
        views.ExtractQueryDescriptionView.as_view(), name='extract_query_description'),
    url(
        r'^search/api/extract_query_schema/$',
        api.ExtractQuerySchemaViewSet.as_view({'get': 'list'}),
        name="extract-query-list"
    ),
    url(
        r'^search/api/extract_slice_schema/$',
        api.ExtractSliceSchemaViewSet.as_view({'get': 'list'}),
        name="extract-slice-list"
    ),
    url(
        r'^search/api/extract_query/(?P<pk>[0-9]+)/',
        api.ExtractQueryViewSet.as_view({'get': 'retrieve'}),
        name="extract-query-detail"
    ),
]
