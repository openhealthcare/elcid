from elcid.management.commands.create_random_data import (
    PatientGenerator, EpisodeSubrecordGenerator, PatientSubrecordGenerator
)
from opal.core.test import OpalTestCase
from elcid.models import Location, ContactDetails, Travel
from opal import models as omodels


class TestPatientGenerator(OpalTestCase):
    FAKE_TAG = "fake_patient"

    def setUp(self, *args, **kwargs):
        omodels.Team.objects.create(name=self.FAKE_TAG)
        omodels.Destination.objects.create(name="somewhere")
        super(TestPatientGenerator, self).setUp(*args, **kwargs)

    def test_patient_generator(self):
        p = PatientGenerator()
        patient = p.make(tags=[self.FAKE_TAG])
        demographics = patient.demographics_set.first()
        self.assertTrue(bool(demographics.date_of_birth))
        self.assertTrue(len(demographics.name))
        self.assertTrue(len(demographics.gender))
        self.assertTrue(len(demographics.hospital_number))
        self.assertTrue(len(demographics.nhs_number))
        episode = patient.episode_set.first()
        self.assertTrue(episode.date_of_admission or episode.date_of_episode)

    def test_episode_subrecord_creator(self):
        p = PatientGenerator()
        patient = p.make([self.FAKE_TAG])
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

    def test_patient_subrecord_creator(self):
        p = PatientGenerator()
        patient = p.make([self.FAKE_TAG])
        episode = patient.episode_set.first()
        e = PatientSubrecordGenerator(ContactDetails, patient)
        e.PROB_OF_NONE = 0
        subrecord = e.make()
        self.assertTrue(bool(subrecord))
        self.assertTrue(bool(subrecord.address_line1))
