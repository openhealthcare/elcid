"""
Referral routes for elCID
"""
from constants import MICROHAEM_TEAM_NAME
from referral import ReferralRoute
from elcid.models import Diagnosis


class MicroHaematology(ReferralRoute):
    name = 'MicroHaematology'
    description = 'The Micro - Haematology service at UCLH'
    target_teams = [MICROHAEM_TEAM_NAME]
    create_new_episode = False
    additional_models = [
        Diagnosis
    ]

    def get_success_link(self, episode):
        return '/#/patient/%s' % episode.patient.id
