import datetime
from collections import OrderedDict
from opal.core.test import OpalTestCase
from opal import models as opal_models
from elcid import models as elcid_models
from opat import models as opat_models
from opat import nors_utils


class AbstractNorsUtilsTestCase(OpalTestCase):
    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        opal_models.Antimicrobial_route.objects.create(name="IV")
        elcid_models.Drug_delivered.objects.create(name="Inpatient Team")
        self.opat_clinic = elcid_models.Drug_delivered.objects.create(name="OPAT Clinic")

        self.fucidin = opal_models.Antimicrobial.objects.create(
            name="fucidin"
        )
        self.paracetomol = opal_models.Antimicrobial.objects.create(
            name="paracetomol"
        )
        self.episode_qs = opal_models.Episode.objects.filter(
            id=self.episode.id
        )
        self.bacteraemia = opat_models.OPATInfectiveDiagnosis.objects.create(
            name="Bacteraemia"
        )
        self.other_diagnosis = opat_models.OPATInfectiveDiagnosis.objects.create(
            name="other_diagnosis"
        )
        self.opat_outcome = opat_models.OPATOutcome.objects.create(
            episode=self.episode,
            opat_outcome=opat_models.OPATOutcome.OPAT_OUTCOME_CHOICES[0][0],
            patient_outcome=opat_models.OPATOutcome.PATIENT_OUTCOME_CHOICES[0][0],
            outcome_stage=nors_utils.COMPLETED_THERAPY_STAGE
        )


class GetPrimaryInfectiveDiagnosisTestCase(AbstractNorsUtilsTestCase):

    def test_get_primary_infective_diagnosis_with_translation(self):
        self.opat_outcome.infective_diagnosis = self.bacteraemia.name
        self.opat_outcome.save()
        result = nors_utils.get_primary_infective_diagnosis(self.episode_qs)
        expected = [
            OrderedDict([
                ('diagnosis', 'bacteraemia / blood stream infection / septicaemia'),
                ('episode', 1),
                ('time_saved', 0),
                ('opat_outcome__Success', 1),
                ('patient_outcome__Cured', 1)
            ])
        ]
        self.assertEqual(result, expected)

    def test_get_primary_infective_diagnosis_without_translation(self):
        self.opat_outcome.infective_diagnosis = self.other_diagnosis.name
        self.opat_outcome.save()
        result = nors_utils.get_primary_infective_diagnosis(self.episode_qs)
        expected = [
            OrderedDict([
                ('diagnosis', 'other_diagnosis'),
                ('episode', 1),
                ('time_saved', 0),
                ('opat_outcome__Success', 1),
                ('patient_outcome__Cured', 1)
            ])
        ]
        self.assertEqual(result, expected)


class AntimicrobialTestCase(AbstractNorsUtilsTestCase):
    def setUp(self):
        super(AntimicrobialTestCase, self).setUp()
        today = datetime.date.today()
        self.antimicrobial = elcid_models.Antimicrobial(
            start_date=today - datetime.timedelta(2),
            end_date=today,
            episode=self.episode
        )
        self.antimicrobial.route = self.opat_clinic.name
        self.antimicrobial.save()

    def test_get_drug_name_with_translation(self):
        self.antimicrobial.drug = self.fucidin.name
        self.antimicrobial.save()
        result = nors_utils.get_drug_name(self.antimicrobial)
        self.assertEqual(
            result, 'fusidic acid'
        )

    def test_get_drug_name_without_translation(self):
        self.antimicrobial.drug = self.paracetomol.name
        self.antimicrobial.save()
        result = nors_utils.get_drug_name(self.antimicrobial)
        self.assertEqual(
            result, 'paracetomol'
        )


class GetEpisodeBreakdownTestCase(AbstractNorsUtilsTestCase):
    def test_episodes_included(self):
        today = datetime.date.today()
        antimicrobial = elcid_models.Antimicrobial(
            start_date=today - datetime.timedelta(2),
            end_date=today,
            episode=self.episode
        )
        antimicrobial.delivered_by = self.opat_clinic.name
        antimicrobial.drug = self.fucidin.name
        antimicrobial.save()

        outcome = opat_models.OPATOutcome.objects.create(
            episode=self.episode,
            opat_outcome=opat_models.OPATOutcome.OPAT_OUTCOME_CHOICES[0][0],
            patient_outcome=opat_models.OPATOutcome.PATIENT_OUTCOME_CHOICES[0][0]
        )
        outcome.infective_diagnosis = "cold"
        outcome.save()
        result = nors_utils.get_episode_breakdown(opal_models.Episode.objects.all())
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(
            row["episode"], "http://elcidl/#/patient/{}/{}".format(
                self.patient.id, self.episode.id
            )
        )

        self.assertEqual(
            row["duration"], 3
        )

        self.assertEqual(
            row["antimicrobials"], 'fusidic acid(3 days)'
        )
        self.assertEqual(
            row["infective_diagnosis"], 'other'
        )
        self.assertEqual(
            row["opat_outcome"], opat_models.OPATOutcome.OPAT_OUTCOME_CHOICES[0][0]
        )

        self.assertEqual(
            row["patient_outcome"], opat_models.OPATOutcome.PATIENT_OUTCOME_CHOICES[0][0]
        )


