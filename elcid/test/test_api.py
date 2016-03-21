from mock import MagicMock, patch

from django.test import override_settings
from django.core.urlresolvers import reverse

from opal.core.test import OpalTestCase
from opal.models import Patient
from opal.tests.models import HatWearer


from elcid.api import GlossEndpointApi


class TestPatientApi(OpalTestCase):
    def test_nonexisting_patient(self):
        endpoint = GlossEndpointApi()

        with patch.object(endpoint, "login") as login_method:
            login_method.return_value = self.user
            request = MagicMock()
            request.data = dict(data={
                "demographics": [{
                    "name": "Susan",
                    "hospital_number": "12312312",
                }],
                "hat_wearer": [
                    {"name": "top"},
                    {"name": "wizard"},
                ]
            })

            endpoint.update(request, pk="12312312")
            patient = Patient.objects.get()
            demographics = patient.demographics_set.get()
            self.assertEqual(demographics.name, "Susan")
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
            request.data = dict(data={
                "demographics": [{
                    "name": "Susan",
                    "hospital_number": "12312312",
                }],
                "hat_wearer": [
                    {"name": "top"},
                    {"name": "wizard"},
                ]
            })
            patient_before = Patient.objects.create()
            demographics = patient_before.demographics_set.get()
            demographics.hospital_number = "12312312"
            demographics.name = "Jane"
            demographics.save()

            endpoint.update(request, pk="12312312")
            patient = Patient.objects.get()
            demographics = patient.demographics_set.get()
            self.assertEqual(demographics.name, "Susan")
            self.assertEqual(demographics.hospital_number, "12312312")
            episode = patient.episode_set.get()
            hat_wearers = episode.hatwearer_set.all()
            self.assertEqual(hat_wearers[0].name, "top")
            self.assertEqual(hat_wearers[1].name, "wizard")
