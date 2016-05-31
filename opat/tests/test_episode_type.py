from opal.core.test import OpalTestCase
from opat import models as opat_models
from elcid import models as elcid_models
import datetime


class EpisodeTypeTestCase(OpalTestCase):
    def setUp(self):
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(1)
        patient, self.accepted_episode = self.new_patient_and_episode_please()
        self.accepted_episode.category = "OPAT"
        self.accepted_episode.date_of_episode = self.today
        self.accepted_episode.save()
        location = self.accepted_episode.location_set.first()
        location.opat_acceptance = self.yesterday
        location.save()
        self.rejected_episode = patient.create_episode()
        self.rejected_episode.category = "OPAT"
        opat_models.OPATRejection.objects.create(
            episode = self.rejected_episode,
            date = self.today
        )
        self.rejected_episode.save()

        self.referral_episode = patient.create_episode()
        self.referral_episode.category = "OPAT"
        self.referral_episode.save()
        self.referral_episode.set_tag_names(["opat_referrals"], None)

    def test_rejected_start(self):
        self.assertEqual(self.rejected_episode.start, self.today)

    def test_rejected_end(self):
        self.assertEqual(self.rejected_episode.end, self.today)

    def test_accepted_start(self):
        self.assertEqual(self.accepted_episode.start, self.yesterday)

    def test_accepted_end(self):
        self.assertEqual(self.accepted_episode.end, self.today)

    def test_referral_start(self):
        self.assertEqual(self.referral_episode.start, None)

    def test_referral_end(self):
        self.assertEqual(self.referral_episode.end, None)
