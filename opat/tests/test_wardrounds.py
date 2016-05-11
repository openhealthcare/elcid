"""
Unittests for elcid.opat.wardrounds
"""
import datetime
from mock import MagicMock
from opal.core.test import OpalTestCase
from opal.models import Tagging
from opat import wardrounds
from opat import models


class OPATCurrentListTestCase(OpalTestCase):
    def test_episodes(self):
        patient, episode = self.new_patient_and_episode_please()
        episode.active = True
        episode.save()
        episode.set_tag_names(['opat', 'opat_current'], self.user)
        mock_request = MagicMock()
        wardround = wardrounds.OPATCurrentList(mock_request)
        self.assertEqual(episode, wardround.episodes().get())


class OPATReviewListTestCase(OpalTestCase):
    def test_episodes(self):
        yesterday = datetime.date.today() - datetime.timedelta(1)
        patient, episode = self.new_patient_and_episode_please()
        models.OPATMeta.objects.create(episode=episode, review_date=yesterday)
        mock_request = MagicMock()
        wardround = wardrounds.OPATReviewList(mock_request)
        self.assertEqual(episode, wardround.episodes().get())
