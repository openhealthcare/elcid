"""
Plugin definition for the opat OPAL plugin
"""
from opal.core import episodes, plugins
from opat.urls import urlpatterns


class OpatPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our OPAL application.
    """
    urls = urlpatterns
    javascripts = {
        'opal.controllers': [
            'js/opat/controllers/opat_referral.js',
            'js/opat/controllers/opat_discharge.js'
        ],
        'opal.opat': [
            # 'js/opat/app.js',
            # 'js/opat/controllers/larry.js',
            # 'js/opat/services/larry.js',
        ]
    }
    actions = (
        'actions/next_stage.html',
        'actions/opat_discharge_summary.html'
    )

    def restricted_teams(self, user):
        """
        Return any restricted teams for particualr users that our
        plugin may define.
        """
        return []

    def list_schemas(self):
        """
        Return any patient list schemas that our plugin may define.
        """
        return {
            "default": list_columns_opat
        }

    def flows(self):
        """
        Return any custom flows that our plugin may define
        """
        flows = {
            'enter': {
                'controller': 'OPATReferralCtrl',
                'template'  : '/opat/templates/modals/opat_referral.html/'
            },
            'exit': {
                'controller': 'OPATDischargeCtrl',
                'template'  : '/opat/templates/modals/discharge_opat_episode.html/'
            }
        }
        return {
            'opat': {
                'default': flows
            },
            'OPAT': flows
        }

    def roles(self, user):
        """
        Given a (Django) USER object, return any extra roles defined
        by our plugin.
        """
        return {}


plugins.register(OpatPlugin)

class OPATEpisode(episodes.EpisodeType):
    name            = 'OPAT'
    detail_template = 'detail/opat2.html'
