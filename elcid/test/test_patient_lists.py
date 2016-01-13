from mock import MagicMock
from opal.core.patient_lists import PatientList
from elcid.patient_lists import Mine
from opal.core.test import OpalTestCase
from opal.models import Patient, Team


class TestPatientList(OpalTestCase):
    def setUp(self):
        self.patient = Patient.objects.create()
        self.episode_1 = self.patient.create_episode()
        self.episode_2 = self.patient.create_episode()

    def test_mine(self):
        ''' given to episodes, calling mine should only return the one tagged with
            the user
        '''
        Team.objects.get_or_create(name="mine")

        self.episode_1.set_tag_names(["mine"], self.user)
        self.assertIn(Mine, PatientList.list_classes())

        mock_request = MagicMock(name='Mock request')
        mock_request.user = self.user

        patient_list = PatientList.get_class(mock_request, tag="mine")
        self.assertEqual(
            [self.episode_1], [i for i in patient_list.get_queryset()]
        )
        serialized = patient_list.get_serialised()
        self.assertEqual(len(serialized), 1)
        self.assertEqual(serialized[0]["id"], 1)
