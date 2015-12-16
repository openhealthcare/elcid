"""
Referral routes for elCID
"""
import datetime
from constants import MICROHAEM_TEAM_NAME

from referral import ReferralRoute
from walkin.models import Management

from elcid.models import MicrobiologyTest, Diagnosis


class HTDWalkInRoute(ReferralRoute):
    name = 'HTD Walk In Clinic'
    description = 'The HTD Walk-In clinic provides a primary care service to returning travelers.'
    target_teams = ['walkin', 'walkin_triage']
    target_category = 'Walkin'
    success_link = '/#/list/walkin'

    def post_create(self, episode, user):
        """
        Auto populate HIV POC
        Set date of appointment to today.
        """
        MicrobiologyTest.objects.create(episode=episode, test='HIV Point of Care')
        episode.date_of_episode = datetime.date.today()
        episode.save()
        return


#class OPATRoute(ReferralRoute):
#    name = 'OPAT'
#    description = 'The Outpatient Parenteral Antibiotic Therapy (OPAT) service at UCLH'
#    target_teams = ['opat', 'opat_referrals']
#    target_category = 'OPAT'
#    success_link = '/#/list/opat'


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
