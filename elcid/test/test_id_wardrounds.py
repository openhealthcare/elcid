"""
Unittests for infectiousdiseases.wardrounds
"""
import datetime

from mock import MagicMock
from opal.core.test import OpalTestCase
from opal.models import Patient

from elcid.models import ConsultantAtDischarge, Consultant
from infectiousdiseases import wardrounds

class ConsultantReviewTestCase(OpalTestCase):
    def test_episodes(self):
        patient, episode = self.new_patient_and_episode_please()
        episode.end = datetime.date.today()
        episode.save()
        dr_watson = Consultant(name='Dr Watson')
        dr_watson.save()
        at_discharge = ConsultantAtDischarge.objects.get(episode=episode)
        at_discharge.consultant='Dr Watson'
        at_discharge.save()
        mock_request = MagicMock()
        mock_request.GET.get.return_value = 'Dr Watson'
        wardround = wardrounds.ConsultantReview(mock_request)
        self.assertEqual(episode, wardround.episodes()[0])
        self.assertEqual(1, wardround.episodes().count())
