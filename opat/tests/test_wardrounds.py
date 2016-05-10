"""
Unittests for elcid.opat.wardrounds
"""
from opal.core.test import OpalTestCase

from opat import wardrounds

class OpatCurrentTestCase(OpalTestCase):
    def test_episodes(self):
        patient, episode = self.new_patient_and_episode_please()
        episode.set_tag_names(['opat', 'opat_current'], self.user)
        self.assertEqual([episode],
                         list(wardrounds.OPATCurrentList(None).episodes()))
