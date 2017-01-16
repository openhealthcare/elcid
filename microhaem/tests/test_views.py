import datetime
from opal.core.test import OpalTestCase
from elcid.test.test_models import AbstractEpisodeTestCase

from microhaem import constants


class MicrobiologyInputViewTest(OpalTestCase, AbstractEpisodeTestCase):
    def setUp(self):
        super(MicrobiologyInputViewTest, self).setUp()
        self.url = "/api/v0.1/microbiology_input/"
        self.assertTrue(self.client.login(username=self.user.username,
                                          password=self.PASSWORD))

        self.args = {
            "clinical_discussion": "something interesting",
            "discussed_with": "Jane",
            "episode_id": self.episode.id,
            "initials": "Jane Doe",
            "reason_for_interaction": constants.MICROHAEM_CONSULTATIONS[0],
            "when": datetime.datetime(2015, 10, 7, 23, 30)
        }

    def test_add_microbiology_input(self):
        tags = self.episode.get_tag_names(self.user)
        self.assertEqual(len(tags), 0)
        self.post_json(self.url, self.args)
        updated_tags = self.episode.get_tag_names(self.user)
        self.assertEqual(
            [str(i) for i in updated_tags], [constants.MICROHAEM_TAG]
        )
        self.post_json(self.url, self.args)

        # make sure tags don't get applied twice if run twice
        updated_tags = self.episode.get_tag_names(self.user)
        self.assertEqual(
            [str(i) for i in updated_tags], [constants.MICROHAEM_TAG]
        )
