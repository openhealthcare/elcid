"""
Plugin definition for elcid search
"""
from search import urls
from opal.core import plugins


class SearchPlugin(plugins.OpalPlugin):
    """
    The plugin entrypoint for OPAL's core search functionality
    """
    urls = urls.urlpatterns
    stylesheets = ["css/search.css"]
    javascripts = {
        'opal.services': [
            ""
            "js/search/services/paginator.js",
            "js/search/services/patient_summary.js",
            "js/search/services/extract_query_schema_loader.js",
            "js/search/services/extract_slice_schema_loader.js",
            "js/search/services/extract_query_loader.js",
            "js/search/services/schema.js",
            "js/search/services/extract_query.js",
        ],
        'opal.controllers': [
            'js/search/app.js',
            'js/search/controllers/search.js',
            'js/search/controllers/extract.js',
        ]
    }
