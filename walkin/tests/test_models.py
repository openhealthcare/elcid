from opal.core.test import OpalTestCase
from walkin import models, patient_lists


class CustomSymptomsModelTestCase(OpalTestCase):

    def test_set_symptom_is_a_dummy(self):
        self.assertEqual(None, models.Symptom().set_symptom())

    def test_get_record_display(self):
        record_template = models.Symptom.get_display_template(
            prefixes=patient_lists.WalkinDoctor().get_template_prefixes()
        )
        self.assertEqual(record_template, "records/symptom.html")
