"""
Referral routes for walkin
"""
import datetime
from referral import ReferralRoute
from elcid.models import MicrobiologyTest


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
        MicrobiologyTest.objects.create(
            episode=episode, test='HIV Point of Care'
        )
        episode.date_of_episode = datetime.date.today()
        episode.save()
        return
