"""
Referral routes for elCID
"""
from microhaem.constants import MICROHAEM_TAG
from referral import ReferralRoute
from elcid.models import Diagnosis


class MicroHaematology(ReferralRoute):
    name = 'MicroHaematology'
    description = 'The Micro - Haematology service at UCLH'
    target_teams = [MICROHAEM_TAG]
    create_new_episode = False
    additional_models = [
        Diagnosis
    ]

    def get_success_link(self, episode):
        return '/#/patient/%s/micro_haem' % episode.patient.id
