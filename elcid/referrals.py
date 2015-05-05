"""
Referral routes for elCID
"""
from referral import ReferralRoute

from elcid.models import MicrobiologyTest

class HTDWalkInRoute(ReferralRoute):
    name = 'HTD Walk In Clinic'
    description = 'The HTD Walk-In clinic provides a primary care service to returning travelers.'
    target_teams = ['walkin', 'walkin_triage']
    target_category = 'Walkin'
    success_link = '/#/list/walkin'

    def post_create(self, episode):
        """
        Auto populate HIV POC
        """
        MicrobiologyTest.objects.create(episode=episode, test='HIV Point of Care')
        return
