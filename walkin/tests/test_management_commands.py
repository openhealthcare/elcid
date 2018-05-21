from datetime import timedelta

from django.core.management import call_command
from django.utils import timezone

from opal.core.test import OpalTestCase
from opal import models as omodels
from elcid.models import PresentingComplaint
from walkin.models import Symptom


class SymptomToPresentingComplaintTest(OpalTestCase):

    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.symptom1 = Symptom.objects.create(
            id=1,
            created=           timezone.now(),
            updated=           timezone.now(),
            created_by=        self.user,
            updated_by=        self.user,
            consistency_token= u'charfield 24167234',
            episode=           self.episode,
            duration=          u'charfield some duration',
            details=           u'some details',
            onset=             u'charfield onset',
            symptom=           u'ftfk symptom',
        )
        self.symptom2 = Symptom.objects.create(
            id=2,
            created=           timezone.now()-timedelta(1),
            updated=           timezone.now()-timedelta(1),
            created_by=        self.user,
            updated_by=        self.user,
            consistency_token= u'charfield 16723461',
            episode=           self.episode,
            duration=          u'charfield some other duration',
            details=           u'some other details',
            onset=             u'charfield some onset',
            symptom=           u'ftfk a different symptom',
        )
        omodels.Symptom.objects.create(name="some_symptom")


    def test_there_are_no_symptom_objects_to_migrate(self):
        self.symptom1.delete()
        self.symptom2.delete()
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.get(details='some details')
        self.assertIsNone(pc1)

    def test_both_symptoms_are_migrated(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.get(id=1)
        pc2 = PresentingComplaint.objects.get(id=2)

        self.assertEqual(self.symptom1.created, pc1.created)
        self.assertEqual(self.symptom1.updated, pc1.updated)
        self.assertEqual(self.symptom1.created_by, pc1.created_by)
        self.assertEqual(self.symptom1.updated_by, pc1.updated_by)
        self.assertEqual(self.symptom1.consistency_token, pc1.consistency_token)
        self.assertEqual(self.symptom1.episode, pc1.episode)
        self.assertEqual(self.symptom1.duration, pc1.duration)
        self.assertEqual(self.symptom1.details, pc1.details)
        self.assertEqual(self.symptom1.onset, pc1.onset)
        self.assertEqual(self.symptom1.symptom_fk_id, pc1.symptom_fk_id)
        self.assertEqual(self.symptom1.symptom_ft, pc1.symptom_ft)

        self.assertEqual(self.symptom2.created, pc2.created)
        self.assertEqual(self.symptom2.updated, pc2.updated)
        self.assertEqual(self.symptom2.created_by, pc2.created_by)
        self.assertEqual(self.symptom2.updated_by, pc2.updated_by)
        self.assertEqual(self.symptom2.consistency_token, pc2.consistency_token)
        self.assertEqual(self.symptom2.episode, pc2.episode)
        self.assertEqual(self.symptom2.duration, pc2.duration)
        self.assertEqual(self.symptom2.details, pc2.details)
        self.assertEqual(self.symptom2.onset, pc2.onset)
        self.assertEqual(self.symptom2.symptom_fk_id, pc2.symptom_fk_id)
        self.assertEqual(self.symptom2.symptom_ft, pc2.symptom_ft)


    def test_symptom_created(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.created, pc1.created)

    def test_symptom_updated(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.updated, pc1.updated)

    def test_symptom_created_by(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.created_by, pc1.created_by)

    def test_symptom_updated_by(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.updated_by, pc1.updated_by)

    def test_symptom_consistency_token(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.consistency_token, pc1.consistency_token)

    def test_symptom_episode(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.episode, pc1.episode)

    def test_symptom_duration(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.duration, pc1.duration)

    def test_symptom_details(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.details, pc1.details)

    def test_symptom_onset(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.onset, pc1.onset)

    def test_symptom_symptom_fk_id(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.symptom_fk_id, pc1.symptom_fk_id)

    def test_symptom_symptom_ft(self):
        call_command('move_symptoms_to_presentingcomplaints')
        pc1 = PresentingComplaint.objects.first()
        self.assertEqual(self.symptom1.symptom_ft, pc1.symptom_ft)
