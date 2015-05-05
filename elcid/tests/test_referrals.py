"""
Unittests for elcid.referrals
"""
from opal.core.test import OpalTestCase
from opal.models import Patient, Episode
from mock import patch

from elcid import referrals

class WalkinTestCase(OpalTestCase):
    def setUp(self):
        self.patient = Patient.objects.create()
        self.episode = self.patient.create_episode()

    @patch('elcid.referrals.MicrobiologyTest.objects.create')
    def test_hiv_poc(self, create):
        referrals.HTDWalkInRoute().post_create(self.episode)
        create.assert_called_with(episode=self.episode, test='HIV Point of Care')
        
