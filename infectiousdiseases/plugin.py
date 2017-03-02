"""
Plugin definition for the ID Plugin
"""
from opal.core import plugins

class InfectiousDiseasesPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our OPAL application.
    """
    javascripts = {
        'opal.controllers': [
            'js/infectiousdiseases/controllers/tropical_liaison_add_patient.js',
            'js/infectiousdiseases/controllers/tropical_liaison_end_liaison.js',
            'js/infectiousdiseases/controllers/virology_hospital_number.js',
        ]
    }

    actions = (
        'actions/end_tropical_liaison.html',
    )
