import json
# from django.test import override_settings
from mock import MagicMock, patch
from opal.core.test import OpalTestCase
# from opal.models import Patient
# from elcid.models import Allergies, Demographics
#
#
from elcid.api import GlossEndpointApi


class TestEndPoint(OpalTestCase):
    @patch("elcid.api.bulk_create_from_gloss_response")
    def test_create(self, bulk_create):
        request = MagicMock()
        expected_dict = dict(
            messages=[],
            hospital_number="1"
        )
        request.data = json.dumps(expected_dict)
        endpoint = GlossEndpointApi()
        endpoint.create(request)
        bulk_create.assert_called_once_with(expected_dict)
