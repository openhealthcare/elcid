"""
Plugin definition
"""
from opal.core import plugins

from walkin.urls import urlpatterns
from walkin import schema


class WalkinPlugin(plugins.OpalPlugin):
    urls = urlpatterns
    javascripts = {
        'opal.controllers': [
            'js/walkin/controllers/walkin_hospital_number.js',
            'js/walkin/controllers/walkin_discharge.js',
            'js/walkin/controllers/nurse_investigation.js'
        ]
    }
    actions = [
        'actions/walkin_next.html',
        'actions/nurse_investigations.html',
        'actions/discharge_summary.html'
    ]

    def list_schemas(self):
        """
        Return any patient list schemas that our plugin may define.
        """
        return {
            'walkin': {
                'walkin_triage': schema.list_columns_triage,
                'walkin_review': schema.list_columns_walkin_review,
                'default': schema.list_columns_walkin
            }
        }

plugins.register(WalkinPlugin)
