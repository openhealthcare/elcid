"""
Unittests for the elCID.detail module
"""
from opal.core.test import OpalTestCase
from django.test import override_settings


@override_settings(GLOSS_ENABLED=True)
class ResultViewTestCase(OpalTestCase):
    def test_slug(self):
        from elcid import detail
        self.assertEqual('test_results', detail.Result.get_slug())
