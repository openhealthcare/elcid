import json
from mock import MagicMock, patch
from opal.core.test import OpalTestCase
from opal.models import Patient
from elcid.models import Allergies, Demographics


from elcid.api import GlossEndpointApi


class TestAllergyInteraction(OpalTestCase):
    def setUp(self, *args, **kwargs):
        self.patient = Patient.objects.create()
        demographics = self.patient.demographics_set.first()
        demographics.hospital_number = "1"
        demographics.save()
        self.before_allergy = Allergies.objects.create(
            patient=self.patient,
            drug_ft="some drug"
        )
        super(TestAllergyInteraction, self).setUp(*args, **kwargs)

    def run_create(self, some_dict, hospital_number="1"):
        request = MagicMock()
        request.data = json.dumps(dict(
            messages=some_dict,
            hospital_number="1"
        ))

        endpoint = GlossEndpointApi()
        with patch.object(endpoint, "login") as login_method:
            login_method.return_value = self.user
            endpoint.create(request)

    def test_remove_allergies(self):
        # if allergies are present, delete allergies and create new ones
        # also run any other updates that are required
        data = dict(
            demographics=[{
                "first_name": "Susan",
                "hospital_number": "1",
            }],
            allergies=[
                {"allergy_description": "penicillin"},
            ]
        )

        self.run_create(data)
        allergy = Allergies.objects.get()
        self.assertFalse(allergy.id == self.before_allergy.id)
        self.assertEqual(allergy.allergy_description, "penicillin")
        self.assertEqual(
            Demographics.objects.get(hospital_number="1").first_name, "Susan"
        )

    def test_doesnt_remove_allergies(self):
        # if no allergies are present, don't delete allergies, but run
        # the other updates
        data = dict(
            demographics=[{
                "first_name": "Susan",
                "hospital_number": "1",
            }],
        )
        self.run_create(data)
        allergy = Allergies.objects.get()
        self.assertEqual(allergy, self.before_allergy)
        self.assertEqual(
            Demographics.objects.get(hospital_number="1").first_name, "Susan"
        )

    def test_transaction_atomicity(self):
        # if the update fails, make sure we don't delete allergies
        data = dict(
            demographics=[{
                "first_name": "Susan",
                "hospital_number": "1",
            }],
            allergies=[
                {"allergy_description": "penicillin"},
            ]
        )
        with patch(
            "elcid.api.Patient.bulk_update",
            side_effect=ValueError("some error")
        ):
            with self.assertRaises(ValueError):
                self.run_create(data)

        self.assertEqual(
            Demographics.objects.get(hospital_number="1").first_name, ""
        )
        allergy = Allergies.objects.get()
        self.assertEqual(allergy, self.before_allergy)


class TestPatientApi(OpalTestCase):
    def test_nonexisting_patient(self):
        endpoint = GlossEndpointApi()

        with patch.object(endpoint, "login") as login_method:
            login_method.return_value = self.user
            request = MagicMock()
            request.data = json.dumps(dict(
                messages={
                    "demographics": [{
                        "first_name": "Susan",
                        "hospital_number": "12312312",
                    }],
                    "hat_wearer": [
                        {"name": "top"},
                        {"name": "wizard"},
                    ]
                },
                hospital_number="12312312"
            ))

            endpoint.create(request)
            patient = Patient.objects.get()
            demographics = patient.demographics_set.get()
            self.assertEqual(demographics.first_name, "Susan")
            self.assertEqual(demographics.hospital_number, "12312312")
            episode = patient.episode_set.get()
            hat_wearers = episode.hatwearer_set.all()
            self.assertEqual(hat_wearers[0].name, "top")
            self.assertEqual(hat_wearers[1].name, "wizard")

    def test_existing_patient(self):
        endpoint = GlossEndpointApi()

        with patch.object(endpoint, "login") as login_method:
            login_method.return_value = self.user
            request = MagicMock()
            request.data = json.dumps(dict(
                messages={
                    "demographics": [{
                        "first_name": "Susan",
                        "hospital_number": "12312312",
                    }],
                    "hat_wearer": [
                        {"name": "top"},
                        {"name": "wizard"},
                    ],
                },
                hospital_number="12312312"
            ))
            patient_before = Patient.objects.create()
            demographics = patient_before.demographics_set.get()
            demographics.hospital_number = "12312312"
            demographics.first_name = "Jane"
            demographics.save()

            endpoint.create(request)
            patient = Patient.objects.get()
            demographics = patient.demographics_set.get()
            self.assertEqual(demographics.first_name, "Susan")
            self.assertEqual(demographics.hospital_number, "12312312")
            episode = patient.episode_set.get()
            hat_wearers = episode.hatwearer_set.all()
            self.assertEqual(hat_wearers[0].name, "top")
            self.assertEqual(hat_wearers[1].name, "wizard")
