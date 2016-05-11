"""
Unittests for elcid.wardrounds
"""
import datetime

from mock import MagicMock
from opal.core.test import OpalTestCase
from opal.models import Tagging
from elcid import wardrounds


class DischargedLastWeekTestCase(OpalTestCase):
    def test_episodes(self):
        patient, episode_1 = self.new_patient_and_episode_please()
        today = datetime.date.today()

        # this is the episode we should see
        episode_1.discharge_date = today
        episode_1.save()
        Tagging.objects.create(value="id_inpatients", episode=episode_1)

        # this is an episode we should not see with a filter
        episode_2 = patient.create_episode()
        episode_2.discharge_date = today
        episode_2.save()
        Tagging.objects.create(value="id_liason", episode=episode_2)

        # this episode is older than 2 weeks
        old_epiosde = patient.create_episode()
        old_epiosde.discharge_date = today - datetime.timedelta(30)
        old_epiosde.save()

        # this episode is not discharged
        patient.create_episode()

        # this episode is opat
        opat_episode = patient.create_episode()
        opat_episode.category = 'OPAT'
        opat_episode.save()

        # without filter
        mock_request = MagicMock()
        mock_request.GET.get.return_value = None
        wardround = wardrounds.Discharged(mock_request)
        self.assertEqual(
            set([episode_1, episode_2]), set(wardround.episodes())
        )

        mock_request = MagicMock()
        mock_request.GET.get.return_value = 'id_inpatients'
        wardround = wardrounds.Discharged(mock_request)
        self.assertEqual(episode_1, wardround.episodes().get())
