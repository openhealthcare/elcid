from mock import patch, MagicMock

from rest_framework.reverse import reverse

from search import api
from opal.core.test import OpalTestCase
from opal.tests.models import HatWearer


class ExtractSchemaTestCase(OpalTestCase):
    def setUp(self):
        self.request = self.rf.get("/")
        self.request.user = self.user

    @patch('search.api.SearchRule.get_schemas')
    def test_records(self, get_schemas):
        get_schemas.return_value = [{}]
        request = self.rf.get("/")
        request.user = self.user
        self.assertEqual(
            [{}],
            api.ExtractSchemaViewSet().list(self.request).data
        )


class DataDictionaryTestCase(OpalTestCase):
    @patch('search.api.ExtractSerializer')
    def test_records(self, serializer):
        serializer.get_schemas.return_value = [{}]
        request = MagicMock()
        request.user = self.user
        self.assertEqual([{}], api.DataDictionaryViewSet().list(request).data)

    def test_integration_records(self):
        request = MagicMock()
        request.user = self.user
        self.assertTrue(api.DataDictionaryViewSet().list(request).data)


class LoginRequredTestCase(OpalTestCase):
    """
        we expect almost all views to 401
    """
    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.request = self.rf.get("/")
        self.hat_wearer = HatWearer.objects.create(episode=self.episode)

    def get_urls(self):
        return [
            reverse('extract-schema-list', request=self.request),
            reverse('data-dictionary-list', request=self.request),
        ]

    def test_401(self):
        for url in self.get_urls():
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                401
            )
