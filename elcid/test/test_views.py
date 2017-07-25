"""
Unittests for the UCLH eLCID OPAL implementation.
"""
import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import ffs

from opal.core.test import OpalTestCase
from opal.models import Patient
from opal.core.subrecords import subrecords
from opal.core.patient_lists import PatientList

from elcid import views


HERE = ffs.Path.here()
TEST_DATA = HERE/'test_data'


class TempPasswordTestCase(OpalTestCase):

    def test_temp_pw(self):
        pw = views.temp_password()
        int_section, word_section = int(pw[:2]), pw[2:]
        self.assertTrue(int_section < 100)
        self.assertTrue(int_section > 9)
        self.assertIn(word_section, ['womble', 'bananas', 'flabbergasted', 'kerfuffle'])


class ViewsTest(OpalTestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.assertTrue(self.client.login(username=self.user.username,
                                          password=self.PASSWORD))
        self.patient = Patient.objects.get(pk=1)

    def test_try_to_create_episode_for_existing_patient_with_active_episode(self):
        data = {
            'demographics': self.patient.demographics_set.get().to_dict(self.user),
            'location': {
                'category': 'Inpatient',
                'hospital': 'UCH',
                'ward': 'T13',
                'bed': 10
                },
            'tagging': {}
            }
        response = self.post_json('/api/v0.1/episode/', data)
        self.assertEqual(201, response.status_code)

    def test_create_episode_for_new_patient(self):
        data = {
            'demographics': {
                'hospital_number': 'BB2222',
                'first_name': 'Johann',
                'surname': 'Schmidt',
                'date_of_birth': '01/06/1970'
                },
            'location': {
                'category': 'Inpatient',
                'hospital': 'UCH',
                'ward': 'T13',
                'bed': 10
                },
            'tagging': {}
            }
        response = self.post_json('/api/v0.1/episode/', data)
        self.assertEqual(201, response.status_code)

    def test_create_episode_for_patient_without_hospital_number(self):
        data = {
            'demographics': {
                'hospital_number': '',
                'first_name': 'Johann',
                'surname': 'Schmidt',
                'date_of_birth': '01/06/1970'
                },
            'location': {
                'category': 'Inpatient',
                'hospital': 'UCH',
                'ward': 'T13',
                'bed': 10
                },
            'tagging': {}
            }
        response = self.post_json('/api/v0.1/episode/', data)
        self.assertEqual(201, response.status_code)

    def test_try_to_update_nonexistent_demographics_subrecord(self):
        response = self.put_json('/api/v0.1/demographics/1234/', {})
        self.assertEqual(404, response.status_code)

    def test_episode_detail_template_view(self):
        self.assertStatusCode('/templates/episode_detail.html/1', 200)

    def test_discharge_patient_template_view(self):
        self.assertStatusCode('/templates/modals/discharge_episode.html/', 200)

    def test_delete_item_confirmation_template_view(self):
        self.assertStatusCode('/templates/modals/delete_item_confirmation.html/', 200)

    def test_all_modal_templates(self):
        """ This renders all of our modal templates and blows up
            if they fail to render
        """
        for i in subrecords():
            if i.get_form_template():
                url = reverse("{}_modal".format(i.get_api_name()))
                self.assertStatusCode(url, 200)

        for p in PatientList.list():
            for i in subrecords():
                if i.get_form_template():
                    url = reverse(
                        "{}_modal".format(i.get_api_name()),
                        kwargs={"list": p.get_slug()}
                    )
                    self.assertStatusCode(url, 200)


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


class BulkCreateUserViewTestCase(OpalTestCase):
    def setUp(self):
        self.url = reverse("bulk-create-users")

    def test_form(self):
        self.assertTrue(
            self.client.login(
                username=self.user.username,
                password=self.PASSWORD
            )
        )
        response = self.client.post(self.url)
        self.assertFalse(response.context_data["form"].is_valid())
        self.assertEqual(response.status_code, 200)

    def test_authenticated(self):
        response = self.client.post(self.url, follow=True)
        login = reverse('admin:login')
        self.assertEqual(response.request["PATH_INFO"], login)

    def test_authenticated_staff(self):
        user = User.objects.create(
            username="someone",
        )
        user.set_password("someone")
        user.save()
        self.assertTrue(
            self.client.login(
                username="someone",
                password="someone"
            )
        )
        response = self.client.post(self.url, follow=True)
        login = reverse('admin:login')
        self.assertEqual(response.request["PATH_INFO"], login)
