"""
Unittests for the microhaem.detail module
"""
from opal.core.test import OpalTestCase

from microhaem import detail

class PatientViewTestCase(OpalTestCase):

    def test_not_visible_by_default(self):
        view = detail.MicroHaemPatientView()
        self.assertEqual(False, view.visible_to(self.user))
