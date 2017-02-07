"""
Plugin definition for the opat OPAL plugin
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
        ]
    }

    actions = (
        'actions/end_tropical_liaison.html',
    )

    def restricted_teams(self, user):
        """
        Return any restricted teams for particualr users that our
        plugin may define.
        """
        return []

    def roles(self, user):
        """
        Given a (Django) USER object, return any extra roles defined
        by our plugin.
        """
        return {}



plugins.register(InfectiousDiseasesPlugin)
