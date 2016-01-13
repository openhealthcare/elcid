from mock import patch
from opal.core.test import OpalTestCase
from opal import models as omodels
from elcid.management.commands.create_random_data import (
    PatientGenerator, EpisodeSubrecordGenerator, PatientSubrecordGenerator,
    TagGenerator
)
from elcid.models import Location, ContactDetails, Travel


class TestPatientGenerator(OpalTestCase):
    FAKE_TAG = "fake_patient"

    def setUp(self, *args, **kwargs):
        omodels.Team.objects.create(name=self.FAKE_TAG)
        omodels.Destination.objects.create(name="somewhere")
        super(TestPatientGenerator, self).setUp(*args, **kwargs)

    @patch("elcid.management.commands.create_random_data.TagGenerator.tag_episode")
    def test_patient_generator(self, m):
        p = PatientGenerator()
        patient = p.make()
        demographics = patient.demographics_set.first()
        self.assertTrue(bool(demographics.date_of_birth))
        self.assertTrue(len(demographics.name))
        self.assertTrue(len(demographics.gender))
        self.assertTrue(len(demographics.hospital_number))
        self.assertTrue(len(demographics.nhs_number))
        episode = patient.episode_set.first()
        self.assertTrue(episode.date_of_admission or episode.date_of_episode)

    @patch("elcid.management.commands.create_random_data.TagGenerator.tag_episode")
    def test_episode_subrecord_creator(self, m):
        p = PatientGenerator()
        patient = p.make()
        episode = patient.episode_set.first()
        e = EpisodeSubrecordGenerator(Location, episode)
        e.PROB_OF_NONE = 0
        subrecord = e.make()
        self.assertTrue(bool(subrecord))
        # check chars are populated
        self.assertTrue(bool(subrecord.category))
        # check text fields are populated
        self.assertTrue(bool(subrecord.opat_referral_team_address))
        # check date fields are populated
        self.assertTrue(bool(subrecord.opat_referral))

        e = EpisodeSubrecordGenerator(Travel, episode)
        e.PROB_OF_NONE = 0
        subrecord = e.make()
        # check foreign key or free text are populated
        self.assertTrue(bool(subrecord.destination))
        # check boolean fields are populated
        did_not_travel = subrecord.did_not_travel == False or subrecord.did_not_travel == True
        self.assertTrue(did_not_travel)

    @patch("elcid.management.commands.create_random_data.TagGenerator.tag_episode")
    def test_patient_subrecord_creator(self, m):
        p = PatientGenerator()
        patient = p.make()
        e = PatientSubrecordGenerator(ContactDetails, patient)
        e.PROB_OF_NONE = 0
        subrecord = e.make()
        self.assertTrue(bool(subrecord))
        self.assertTrue(bool(subrecord.address_line1))

    def test_tagger(self):
        patient = omodels.Patient.objects.create()
        episode = patient.create_episode()
        omodels.Team.objects.create(name="test_something")
        omodels.Team.objects.create(name="test_something_else")
        t = TagGenerator()
        t.unique_together = [
            ("test_something",)
        ]
        t.category_map = {
            "test": "tester"
        }

        t.tag_episode(episode)
        self.assertEqual(episode.category, "tester")
        self.assertEqual(list(episode.get_tag_names(None)), [u'test_something'])

        t.unique_together = [None]
        t.tag_episode(episode)
        other_tag_names = episode.get_tag_names(None)

        self.assertTrue(
            "test_something_else" in other_tag_names or self.FAKE_TAG in other_tag_names
        )
