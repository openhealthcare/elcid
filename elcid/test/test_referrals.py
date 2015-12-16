"""
Unittests for elcid.referrals
"""
import datetime

from opal.core.test import OpalTestCase
from opal.models import Patient, Episode
from mock import patch

from elcid import referrals

TODAY = datetime.date.today()

class WalkinTestCase(OpalTestCase):
    def setUp(self):
        self.patient = Patient.objects.create()
        self.episode = self.patient.create_episode()

    @patch('elcid.referrals.MicrobiologyTest.objects.create')
    def test_hiv_poc(self, create):
        referrals.HTDWalkInRoute().post_create(self.episode, None)
        create.assert_called_with(episode=self.episode, test='HIV Point of Care')
        
    @patch('elcid.referrals.Management.objects.create')        
    def test_date_of_appointment(self, create):
        referrals.HTDWalkInRoute().post_create(self.episode, None)
        self.assertEqual(TODAY, self.episode.date_of_episode)

