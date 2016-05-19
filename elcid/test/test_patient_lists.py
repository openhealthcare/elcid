from mock import MagicMock

from django.test import RequestFactory
from django.core.urlresolvers import reverse
from opal.core.patient_lists import PatientList
from rest_framework.reverse import reverse as drf_reverse
from opal.core.test import OpalTestCase
from opal.models import Patient

from elcid.patient_lists import Mine


class TestPatientList(OpalTestCase):
    def setUp(self):
        self.patient = Patient.objects.create()
        self.episode_1 = self.patient.create_episode()
        self.episode_2 = self.patient.create_episode()
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )
        self.factory = RequestFactory()

    def test_mine(self):
        ''' given to episodes, calling mine should only return the one tagged with
            the user
        '''
        self.episode_1.set_tag_names(["mine"], self.user)
        self.assertIn(Mine, PatientList.list())

        mock_request = MagicMock(name='Mock request')
        mock_request.user = self.user

        patient_list = PatientList.get("mine")()
        self.assertEqual(
            [self.episode_1], [i for i in patient_list.get_queryset()]
        )
        serialized = patient_list.to_dict(self.user)
        self.assertEqual(len(serialized), 1)
        self.assertEqual(serialized[0]["id"], 1)

    def test_get_all_patient_lists(self):
        # this should not be taken as a reason not to do more indepth unit tests!
        # its just a nice sanity check
        patient_lists = PatientList.list()
        for pl in patient_lists:
            slug = pl.get_slug()
            url = reverse(
                "patient_list_template_view", kwargs={"slug": slug}
            )

            self.assertStatusCode(
                url, 200,
                msg="Failed to load the template for {}".format(slug)
            )

    def test_get_all_patient_api(self):
        # this should not be taken as a reason not to do more indepth unit tests!
        # its just a nice sanity check
        patient_lists = PatientList.list()
        request = self.factory.get("/")
        request.user = self.user
        for pl in patient_lists:
            slug = pl.get_slug()
            url = drf_reverse(
                "patientlist-detail", kwargs={"pk": slug}, request=request
            )

            self.assertStatusCode(
                url, 200,
                msg="Failed to load the template for {}".format(slug)
            )
