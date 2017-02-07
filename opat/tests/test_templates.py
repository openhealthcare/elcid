"""
Test that the templates we need are here
"""
from django.contrib.auth.models import User
from django.test import TestCase

from opat.plugin import OpatPlugin

class FlowTemplatesTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()
        self.flows = OpatPlugin().flows()

    def test_enter_template(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.flows['opat']['default']['enter']['template'])
        self.assertEqual(200, response.status_code)

    def test_enter_template_unauthenticated(self):
        response = self.client.get(self.flows['opat']['default']['enter']['template'])
        self.assertEqual(302, response.status_code)

    def test_exit_template(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.flows['opat']['default']['exit']['template'])
        self.assertEqual(200, response.status_code)

    def test_exit_template_unauthenticated(self):
        response = self.client.get(self.flows['opat']['default']['exit']['template'])
        self.assertEqual(302, response.status_code)
