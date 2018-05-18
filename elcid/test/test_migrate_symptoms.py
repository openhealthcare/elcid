from mock import MagicMock
from opal.core.test import OpalTestCase
from opal.models import Symptom
from elcid.models import PresentingComplaint
from walkin.models import Symptom as Symptoms
from elcid.migrations.utils import migrate_symptom


class MigrationTestCase(OpalTestCase):
    def setUp(self):
        _, self.episode = self.new_patient_and_episode_please()
        self.symptom_1 = Symptom.objects.create(name="Cough")
        self.symptom_2 = Symptom.objects.create(name="Itching")
        model_dict = dict(
            PresentingComplaint=PresentingComplaint,
            Symptom=Symptoms
        )
        get_app = lambda x, y: model_dict[y]
        self.apps_mock = MagicMock()
        self.apps_mock.get_model.side_effect = get_app

    def test_presenting_complaint_symptom_migration(self):
        PresentingComplaint.objects.create(
            episode=self.episode,
            symptom_fk=self.symptom_1
        )
        migrate_symptom.migrate_forwards(self.apps_mock)
        presenting_compaint = PresentingComplaint.objects.get()
        self.assertEqual(
            presenting_compaint.symptoms.get(), self.symptom_1
        )

    def test_symptoms_migration(self):
        Symptoms.objects.create(
            episode=self.episode,
            symptom_fk=self.symptom_1
        )
        migrate_symptom.migrate_forwards(self.apps_mock)
        symptoms = Symptoms.objects.get()
        self.assertEqual(
            symptoms.symptoms.get(), self.symptom_1
        )

    def test_no_symptom(self):
        PresentingComplaint.objects.create(
            episode=self.episode,
        )
        migrate_symptom.migrate_forwards(self.apps_mock)
        presenting_compaint = PresentingComplaint.objects.get()
        self.assertFalse(presenting_compaint.symptoms.exists())

    def test_no_symptom_existing_symptoms(self):
        pc = PresentingComplaint.objects.create(
            episode=self.episode,
        )
        pc.symptoms.add(self.symptom_1)
        migrate_symptom.migrate_forwards(self.apps_mock)
        presenting_compaint = PresentingComplaint.objects.get()
        self.assertEqual(
            presenting_compaint.symptoms.get(), self.symptom_1
        )

    def test_symptom_existing_symptoms(self):
        pc = PresentingComplaint.objects.create(
            episode=self.episode,
            symptom_fk=self.symptom_1
        )
        pc.symptoms.add(self.symptom_2)

        migrate_symptom.migrate_forwards(self.apps_mock)
        presenting_compaint = PresentingComplaint.objects.get()
        found_symptoms = set(
            presenting_compaint.symptoms.all().values_list("name", flat=True)
        )
        self.assertEqual(
            found_symptoms, {self.symptom_1.name, self.symptom_2.name}
        )

    def test_presenting_complaint_symptom_already_in_symptoms(self):
        pc = PresentingComplaint.objects.create(
            episode=self.episode,
            symptom_fk=self.symptom_1
        )
        pc.symptoms.add(self.symptom_1)
        migrate_symptom.migrate_forwards(self.apps_mock)
        presenting_compaint = PresentingComplaint.objects.get()
        self.assertEqual(
            presenting_compaint.symptoms.get(), self.symptom_1
        )
