from opal.core.test import OpalTestCase
from opal.models import Patient
from django.core.urlresolvers import reverse
from microhaem import pathways
from elcid.models import Diagnosis


class HaemPathwayTestCase(OpalTestCase):
    def setUp(self):
        self.pathway = pathways.HaemReferalPathway()

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
        old_patient.demographics_set.update(
            hospital_number="100"
        )
        old_episode.set_tag_names(["something"], self.user)
        self.pathway.save({
            "demographics": [
                old_patient.demographics_set.first().to_dict(self.user)
            ],
            "diagnosis": [{"condition": "sick"}]
        }, user=self.user, patient=old_patient, episode=old_episode)
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

    def test_save_with_episode_with_diagnosis(self):
        old_patient, old_episode = self.new_patient_and_episode_please()
        diagnosis = old_episode.diagnosis_set.create()
        diagnosis.condition = "cough"
        diagnosis.save()
        old_episode.set_tag_names(["something"], self.user)
        self.pathway.save({
            "demographics": [{"hospital_number": "100"}],
            "diagnosis": [
                diagnosis.to_dict(self.user),
                {"condition": "sick", "episode_id": old_episode.id}
            ]
        }, user=self.user, patient=old_patient, episode=old_episode)
        patient = Patient.objects.get()
        episode = patient.episode_set.first()
        self.assertEqual(
            patient.demographics_set.first().hospital_number,
            "100"
        )
        self.assertEqual(
            episode.diagnosis_set.count(),
            2
        )
        self.assertEqual(
            episode.diagnosis_set.first().condition,
            "cough"
        )
        self.assertEqual(
            episode.diagnosis_set.last().condition,
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
