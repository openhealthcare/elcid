from opal.core.test import OpalTestCase
from opal.models import Patient
from django.core.urlresolvers import reverse
from microhaem import pathways


class HaemPathwayTestCase(OpalTestCase):
    def setUp(self):
        self.pathway = pathways.ReferPatientPathway()

    def test_render(self):
        url = reverse('pathway_template', kwargs=dict(name='haem_referral'))
        self.assertStatusCode(url, 200)

    def test_save(self):
        self.pathway.save({
            "demographics": [{"hospital_number": "100"}],
            "diagnosis": [{"condition": "sick"}]
        })
        patient = Patient.objects.get()
        episode = patient.episode_set.first()
        self.assertEqual(
            patient.demographics_set.first().hospital_number,
            "100"
        )
        self.assertEqual(
            episode.diagnosis_set.first().condition,
            "sick"
        )
        self.assertEqual(
            list(episode.get_tag_names(None)),
            ["micro_haem"]
        )

    def test_save_with_episode(self):
        old_patient, old_episode = self.new_patient_and_episode_please()
        old_episode.set_tag_names(["something"], self.user)
        self.pathway.save({
            "demographics": [{"hospital_number": "100"}],
            "diagnosis": [{"condition": "sick"}]
        }, user=self.user, patient=old_patient)
        patient = Patient.objects.get()
        episode = patient.episode_set.first()
        self.assertEqual(
            patient.demographics_set.first().hospital_number,
            "100"
        )
        self.assertEqual(
            episode.diagnosis_set.first().condition,
            "sick"
        )
        self.assertEqual(
            list(episode.get_tag_names(None)),
            ["something", "micro_haem"]
        )

    def test_redirect_url(self):
        patient, _ = self.new_patient_and_episode_please()
        self.assertEqual(
            self.pathway.redirect_url(patient=patient),
            "/#/patient/1/micro_haem"
        )
