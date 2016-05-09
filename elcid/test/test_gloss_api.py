import json
from django.test import override_settings
from mock import patch, MagicMock
from opal.core.test import OpalTestCase
from opal.models import Patient, InpatientAdmission
from elcid.models import Allergies, Demographics
from elcid.test.test_models import AbstractEpisodeTestCase
from elcid import gloss_api


@override_settings(
    GLOSS_USERNAME="test_gloss_user",
    GLOSS_PASSWORD="test_gloss_password"
)
class AbstractGlossTestCase(OpalTestCase):
    def setUp(self, *args, **kwargs):
        super(AbstractGlossTestCase, self).setUp(*args, **kwargs)
        self.patient = Patient.objects.create()
        demographics = self.patient.demographics_set.first()
        demographics.hospital_number = "1"
        demographics.save()

    def run_create(self, some_dict, hospital_number="1"):
        episode = self.patient.create_episode()
        expected_request = dict(
            messages=some_dict,
            hospital_number="1"
        )
        gloss_api.bulk_create_from_gloss_response(expected_request, episode)


class TestInpatientAdmission(AbstractGlossTestCase):
    def test_creates_subrecord(self, *args):
        data = dict(
            demographics=[{
                "first_name": "Susan",
                "hospital_number": "1",
            }],
            inpatient_admission=[
                {"hospital": "ucl"},
            ]
        )

        self.run_create(data)
        inpatient_admission = InpatientAdmission.objects.get()
        self.assertEqual(inpatient_admission.hospital, "ucl")
        self.assertEqual(inpatient_admission.external_system, "Carecast")


class TestAllergyInteraction(AbstractGlossTestCase):
    def setUp(self, *args, **kwargs):
        super(TestAllergyInteraction, self).setUp(*args, **kwargs)

        self.before_allergy = Allergies.objects.create(
            patient=self.patient,
            drug_ft="some drug"
        )

    def test_remove_allergies(self, *args):
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

        # all allergies should be marked as having been source
        # from upstream
        self.assertTrue(allergy.sourced_from_upstream)

    def test_doesnt_remove_allergies(self, *args):
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
            "elcid.gloss_api.Patient.bulk_update",
            side_effect=ValueError("some error")
        ):
            with self.assertRaises(ValueError):
                self.run_create(data)

        self.assertEqual(
            Demographics.objects.get(hospital_number="1").first_name, ""
        )
        allergy = Allergies.objects.get()
        self.assertEqual(allergy, self.before_allergy)


@override_settings(
    GLOSS_USERNAME="test_gloss_user",
    GLOSS_PASSWORD="test_gloss_password"
)
class TestPatientApi(OpalTestCase):
    def run_create(self, some_dict, hospital_number="12312312"):
        expected_request = dict(
            messages=some_dict,
            hospital_number=hospital_number
        )
        gloss_api.bulk_create_from_gloss_response(expected_request)

    def test_nonexisting_patient(self, *args):
        request_data = {
            "demographics": [{
                "first_name": "Susan",
                "hospital_number": "12312312",
            }],
            "hat_wearer": [
                {"name": "top"},
                {"name": "wizard"},
            ]
        }
        self.run_create(request_data)
        patient = Patient.objects.get()
        demographics = patient.demographics_set.get()
        self.assertEqual(demographics.first_name, "Susan")
        self.assertEqual(demographics.hospital_number, "12312312")
        episode = patient.episode_set.get()
        hat_wearers = episode.hatwearer_set.all()
        self.assertEqual(hat_wearers[0].name, "top")
        self.assertEqual(hat_wearers[1].name, "wizard")

    def test_existing_patient(self, *args):
        request_data = {
            "demographics": [{
                "first_name": "Susan",
                "hospital_number": "12312312",
            }],
            "hat_wearer": [
                {"name": "top"},
                {"name": "wizard"},
            ],
        }
        patient_before = Patient.objects.create()
        demographics = patient_before.demographics_set.get()
        demographics.hospital_number = "12312312"
        demographics.first_name = "Jane"
        demographics.save()

        self.run_create(request_data)
        patient = Patient.objects.get()
        demographics = patient.demographics_set.get()
        self.assertEqual(demographics.first_name, "Susan")
        self.assertEqual(demographics.hospital_number, "12312312")
        episode = patient.episode_set.get()
        hat_wearers = episode.hatwearer_set.all()
        self.assertEqual(hat_wearers[0].name, "top")
        self.assertEqual(hat_wearers[1].name, "wizard")


class TestPatientQuery(AbstractEpisodeTestCase):

    @override_settings(GLOSS_URL_BASE="http://fake_url.com")
    @patch("elcid.gloss_api.bulk_create_from_gloss_response")
    @patch("elcid.gloss_api.requests.get")
    def test_patient_query_with_error(self, request_mock, bulk_create_mock):
        response = MagicMock()
        response.status_code = 200
        response.content = json.dumps(
            dict(status="error", data="didn't work")
        )
        request_mock.return_value = response
        gloss_api.patient_query("AA1111", self.episode)
        request_mock.assert_called_once_with(
            "http://fake_url.com/api/patient/AA1111"
        )
        self.assertFalse(bulk_create_mock.called)

    @override_settings(GLOSS_URL_BASE="http://fake_url.com")
    @patch("elcid.gloss_api.bulk_create_from_gloss_response")
    @patch("elcid.gloss_api.requests.get")
    def test_patient_query_with_inaccessible_url(
        self, request_mock, bulk_create_mock
    ):
        response = MagicMock()
        response.status_code = 500
        response.content = json.dumps(
            dict(status="error", data="didn't work")
        )
        request_mock.return_value = response
        gloss_api.patient_query("AA1111", self.episode)
        request_mock.assert_called_once_with(
            "http://fake_url.com/api/patient/AA1111"
        )
        self.assertFalse(bulk_create_mock.called)

    @override_settings(GLOSS_URL_BASE="http://fake_url.com")
    @patch("elcid.gloss_api.bulk_create_from_gloss_response")
    @patch("elcid.gloss_api.requests.get")
    def test_patient_query_with_successful_response(
        self, request_mock, bulk_create_mock
    ):
        data = {
            "hospital_number": "AA1111",
            "status": "success",
            "messages": []
        }

        response = MagicMock()
        response.status_code = 200
        response.content = json.dumps(data)
        request_mock.return_value = response
        gloss_api.patient_query("AA1111", self.episode)
        request_mock.assert_called_once_with(
            "http://fake_url.com/api/patient/AA1111"
        )
        bulk_create_mock.assert_called_once_with(data, episode=self.episode)
