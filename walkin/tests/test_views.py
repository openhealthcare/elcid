"""
unittests for walkin.views
"""
from django.contrib.auth.models import User
from opal.core.test import OpalTestCase

class ModalsTestCase(OpalTestCase):

    def setUp(self):
        self.user2 = User.objects.create_user(username='testuser', password='password')

    def test_discharge_template(self):
        self.assertTrue(self.client.login(username='testuser', password='password'))
        self.assertStatusCode('/templates/modals/discharge_walkin_episode.html', 200)

    def test_add_template(self):
        self.assertStatusCode('/templates/modals/add_walkin_episode.html', 200)

    def test_nurse_investigations_view(self):
        self.assertStatusCode('/walkin/modals/nurse_investigations.html', 200)

    def test_modal_render(self):
        url = "/templates/modals/symptom.html/walkin-walkin_triage"
        self.assertStatusCode(url, 200)
