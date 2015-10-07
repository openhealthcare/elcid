"""
Unittests for the UCLH eLCID OPAL implementation.
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import ffs
import random

from opal.core.test import OpalTestCase
from opal.models import Patient

HERE = ffs.Path.here()
TEST_DATA = HERE/'test_data'


class ViewsTest(OpalTestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.assertTrue(self.client.login(username=self.user.username,
                                          password=self.PASSWORD))
        self.patient = Patient.objects.get(pk=1)

    def test_try_to_get_patient_detail_for_nonexistent_patient(self):
        while True:
            rand_int = str(random.randint(0, 2342343))
            if not Patient.objects.filter(hospital_number=rand_int):
                break

        Patient.objects.last().values_list("id")
        url = reverse("patint_detail_data_view", kwargs={
            "hospital_number": rand_int
        })
        self.assertStatusCode(url, 404)

    def test_try_to_create_episode_for_existing_patient_with_active_episode(self):
        data = {
            'demographics': self.patient.demographics_set.get().to_dict(self.user),
            'location': {
                'category': 'Inpatient',
                'hospital': 'UCH',
                'ward': 'T13',
                'bed': 10
                }
            }
        response = self.post_json('/episode/', data)
        self.assertEqual(201, response.status_code)

    def test_create_episode_for_new_patient(self):
        data = {
            'demographics': {
                'hospital_number': 'BB2222',
                'name': 'Johann Schmidt',
                'date_of_birth': '1970-06-01'
                },
            'location': {
                'category': 'Inpatient',
                'hospital': 'UCH',
                'ward': 'T13',
                'bed': 10
                },
            'tagging': [{}]
            }
        response = self.post_json('/episode/', data)
        self.assertEqual(201, response.status_code)

    def test_create_episode_for_patient_without_hospital_number(self):
        data = {
            'demographics': {
                'hospital_number': '',
                'name': 'Johann Schmidt',
                'date_of_birth': '1970-06-01'
                },
            'location': {
                'category': 'Inpatient',
                'hospital': 'UCH',
                'ward': 'T13',
                'bed': 10
                },
            'tagging': [{}]
            }
        response = self.post_json('/episode/', data)
        self.assertEqual(201, response.status_code)

    def test_try_to_update_nonexistent_demographics_subrecord(self):
        response = self.put_json('/api/v0.1/demographics/1234/', {})
        self.assertEqual(404, response.status_code)

    def test_episode_list_template_view(self):
        self.assertStatusCode('/templates/episode_list.html/', 200)

    def test_episode_detail_template_view(self):
        self.assertStatusCode('/templates/episode_detail.html/1', 200)

    def test_patient_notes_template_view(self):
        url = reverse("patient_detail_template_view")
        self.assertStatusCode(url, 200)

    def test_add_patient_template_view(self):
        self.assertStatusCode('/templates/modals/add_episode.html/', 200)

    def test_discharge_patient_template_view(self):
        self.assertStatusCode('/templates/modals/discharge_episode.html/', 200)

    def test_delete_item_confirmation_template_view(self):
        self.assertStatusCode('/templates/modals/delete_item_confirmation.html/', 200)

    def test_location_modal_template_view(self):
        self.assertStatusCode('/templates/modals/location.html/', 200)


class ListSchemaViewTest(OpalTestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.assertTrue(self.client.login(username=self.user.username,
                                          password=self.PASSWORD))
        self.patient = Patient.objects.get(pk=1)
        schema_file = TEST_DATA/'list.schema.json'
        self.schema = schema_file.json_load()

    def assertStatusCode(self, path, expected_status_code):
        response = self.client.get(path)
        self.assertEqual(expected_status_code, response.status_code)


class DetailSchemaViewTest(OpalTestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='password'))
        self.patient = Patient.objects.get(pk=1)
        schema_file = TEST_DATA/'detail.schema.json'
        self.schema = schema_file.json_load()

    def assertStatusCode(self, path, expected_status_code):
        response = self.client.get(path)
        self.assertEqual(expected_status_code, response.status_code)


class ExtractSchemaViewTest(OpalTestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='password'))
        self.patient = Patient.objects.get(pk=1)
        schema_file = TEST_DATA/'extract.schema.json'
        self.schema = schema_file.json_load()

    def assertStatusCode(self, path, expected_status_code):
        response = self.client.get(path)
        self.assertEqual(expected_status_code, response.status_code)
