"""
Plugin definition
"""
from opal.core import plugins, episodes

from research.flow import get_study_flows
from research.roles import get_study_roles
from research.teams import get_study_teams
from research.urls import urlpatterns


class ResearchStudyPlugin(plugins.OpalPlugin):
    urls        = urlpatterns
    javascripts = {
        'opal.controllers': [
            'js/research/controllers/research_hospital_number.js',
            'js/research/controllers/discharge.js'
        ]
    }

    actions = 'actions/remove_research_patient.html',

    def restricted_teams(self, user):
        return get_study_teams(user)

    def flows(self):
        return get_study_flows()

    def roles(self, user):
        return get_study_roles(user)


plugins.register(ResearchStudyPlugin)
