from opal.core.test import OpalTestCase
from walkin import models, patient_lists


class CustomSymptomsModelTestCase(OpalTestCase):
    def test_get_modal_detail(self):
        modal_template = models.Symptom.get_modal_template(
            patient_list=patient_lists.WalkinDoctor()
        )
        self.assertEqual(modal_template, "modals/walkin/symptom_modal.html")

    def test_get_record_display(self):
        record_template = models.Symptom.get_display_template(
            patient_list=patient_lists.WalkinDoctor()
        )
        self.assertEqual(record_template, "records/symptom.html")
