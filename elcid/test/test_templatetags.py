"""
Tests for our modal/form helpers
"""
from django.template import Template, Context
from opal.core.test import OpalTestCase
from elcid.models import Diagnosis


class TestGetStyleTestCase(OpalTestCase):
    def setUp(self):
        tmp = '{% load elcid_pathways %}{% open_multisave subrecord %}'
        self.template = Template(tmp)

    def test_textarea(self):
        rendered = self.template.render(Context(dict(subrecord=Diagnosis)))
        self.assertIn("save-multiple-wrapper", rendered)
