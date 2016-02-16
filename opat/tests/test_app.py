"""
Unittests for opat
"""
from django.test import TestCase

from opat import OpatPlugin

class ApplicationTestCase(TestCase):
    def test_flows(self):
        flows = OpatPlugin().flows()
        self.assertEqual(2, len(flows))
        self.assertIn('enter', flows['opat']['default'].keys())
        self.assertIn('exit', flows['opat']['default'].keys())
