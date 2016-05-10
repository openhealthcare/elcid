"""
Unittests for the elCID.detail module
"""
from opal.core.test import OpalTestCase

from elcid import detail

class ResultViewTestCase(OpalTestCase):
    def test_slug(self):
        self.assertEqual('test_results', detail.Result.get_slug())
