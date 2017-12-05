"""
Plugin definition for the opat OPAL plugin
"""
from opal.core import plugins


class HaemPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our OPAL application.
    """
    javascripts = {
        'opal.controllers': [
            'js/haem/controllers/uch_find_patient.js',
        ],
        'haem.referrals': [
            'js/haem/app.js',
        ]
    }
