import datetime
from collections import OrderedDict
from opal.core.test import OpalTestCase
from opal import models as opal_models
from elcid import models as elcid_models
from opat import models as opat_models
from opat import nors_utils
from opat import quarter_utils


class AbstractNorsUtilsTestCase(OpalTestCase):
    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.iv_route = opal_models.Antimicrobial_route.objects.create(name="IV")
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
            row["antimicrobials"], 'fusidic acid(3)'
        )
        self.assertEqual(
            row["infective_diagnosis"], 'other'
        )
        self.assertEqual(
            row["opat_outcome"],
            opat_models.OPATOutcome.OPAT_OUTCOME_CHOICES[0][0]
        )

        self.assertEqual(
            row["patient_outcome"],
            opat_models.OPATOutcome.PATIENT_OUTCOME_CHOICES[0][0]
        )


class GetDrugCombinationsTestCase(AbstractNorsUtilsTestCase):
    def setUp(self):
        super(GetDrugCombinationsTestCase, self).setUp()
        self.aspirin = opal_models.Antimicrobial.objects.create(
            name="aspirin"
        )
        self.antimicrobial = elcid_models.Antimicrobial.objects.create(
            episode=self.episode
        )
        self.antimicrobial.drug = self.aspirin.name
        self.antimicrobial.save()
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(1)

    def test_generic(self):
        self.antimicrobial.start_date = self.yesterday
        self.antimicrobial.end_date = self.today
        self.antimicrobial.save()
        result = nors_utils.get_drug_combinations([self.antimicrobial])
        drug_combination_keys = list(result.keys())
        self.assertEqual(len(drug_combination_keys), 1)
        drug_combination_key = drug_combination_keys[0]
        self.assertEqual(
            drug_combination_key.start, self.yesterday
        )
        self.assertEqual(
            drug_combination_key.end, self.today
        )
        self.assertEqual(
           result[drug_combination_key],
           [self.antimicrobial.drug]
        )

    def test_drug_combination_hit(self):
        other_antimicrobial = elcid_models.Antimicrobial.objects.create(
            episode=self.episode
        )
        other_antimicrobial.drug = self.paracetomol.name
        other_antimicrobial.start_date = self.yesterday
        other_antimicrobial.end_date = self.today
        other_antimicrobial.save()
        self.antimicrobial.start_date = self.yesterday
        self.antimicrobial.end_date = self.today
        self.antimicrobial.save()

        result = nors_utils.get_drug_combinations([
            self.antimicrobial, other_antimicrobial
        ])
        drug_combination_keys = list(result.keys())
        self.assertEqual(len(drug_combination_keys), 1)
        drug_combination_key = drug_combination_keys[0]
        self.assertEqual(
            drug_combination_key.start, self.yesterday
        )
        self.assertEqual(
            drug_combination_key.end, self.today
        )
        self.assertEqual(
           set(result[drug_combination_key]),
           set([self.antimicrobial.drug, other_antimicrobial.drug])
        )

    def test_drug_combination_miss(self):
        other_antimicrobial = elcid_models.Antimicrobial.objects.create(
            episode=self.episode
        )
        other_antimicrobial.drug = self.paracetomol.name
        two_days_ago = self.yesterday - datetime.timedelta(1)
        other_antimicrobial.start_date = two_days_ago
        other_antimicrobial.end_date = self.today
        other_antimicrobial.save()
        self.antimicrobial.start_date = self.yesterday
        self.antimicrobial.end_date = self.today
        self.antimicrobial.save()

        result = nors_utils.get_drug_combinations([
            self.antimicrobial, other_antimicrobial
        ])
        drug_combination_keys = list(result.keys())
        self.assertEqual(len(drug_combination_keys), 2)

        for drug_combination, drugs in result.items():
            if drugs == [other_antimicrobial.drug]:
                self.assertEqual(
                    drug_combination.start, two_days_ago
                )

                self.assertEqual(
                    drug_combination.end, self.today
                )
            elif drugs == [self.aspirin.name]:
                self.assertEqual(
                    drug_combination.start, self.yesterday
                )

                self.assertEqual(
                    drug_combination.end, self.today
                )
            else:
                self.fail()

    def test_no_start(self):
        self.antimicrobial.start_date = self.yesterday
        self.antimicrobial.save()
        result = nors_utils.get_drug_combinations([self.antimicrobial])
        self.assertEqual(len(result), 0)

    def test_no_end(self):
        self.antimicrobial.end_date = self.yesterday
        self.antimicrobial.save()
        result = nors_utils.get_drug_combinations([self.antimicrobial])
        self.assertEqual(len(result), 0)

    def test_no_duration(self):
        # the day is one day in the future as we
        # consider duration to be start - end + 1
        # ie inclusive of the end date.
        self.antimicrobial.start_date = self.today
        self.antimicrobial.end_date = self.yesterday
        self.antimicrobial.save()
        result = nors_utils.get_drug_combinations([self.antimicrobial])
        self.assertEqual(len(result), 0)


class GetIvAntimicrobialsTestCase(AbstractNorsUtilsTestCase):
    def test_generic(self):
        today = datetime.date.today()
        antimicrobial = elcid_models.Antimicrobial(
            start_date=today - datetime.timedelta(2),
            end_date=today,
            episode=self.episode,
            route_fk_id=self.iv_route.id
        )
        antimicrobial.delivered_by = self.opat_clinic.name
        antimicrobial.drug = self.fucidin.name
        antimicrobial.save()   
        result = nors_utils.get_iv_antimicrobials(
            opal_models.Episode.objects.filter(id=self.episode.id)
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0]["episode_id"], self.episode.id
        )

        self.assertEqual(
            result[0]["max_end"], today
        )

    def test_only_includes_iv_route(self):
        today = datetime.date.today()
        antimicrobial = elcid_models.Antimicrobial(
            start_date=today - datetime.timedelta(2),
            end_date=today - datetime.timedelta(1),
            episode=self.episode,
            route_fk_id=self.iv_route.id
        )
        antimicrobial.delivered_by = self.opat_clinic.name
        antimicrobial.drug = self.fucidin.name
        antimicrobial.save()   

        antimicrobial_other = elcid_models.Antimicrobial(
            start_date=today - datetime.timedelta(2),
            end_date=today,
            episode=self.episode,
        )
        antimicrobial_other.delivered_by = self.opat_clinic.name
        antimicrobial_other.drug = self.fucidin.name
        antimicrobial.route = "other"
        antimicrobial_other.save() 
        result = nors_utils.get_iv_antimicrobials(
            opal_models.Episode.objects.filter(id=self.episode.id)
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0]["episode_id"], self.episode.id
        )

        self.assertEqual(
            result[0]["max_end"], today - datetime.timedelta(1)
        )

    def test_with_none(self):
        result = nors_utils.get_iv_antimicrobials(
            opal_models.Episode.objects.filter(id=self.episode.id)
        )
        self.assertEqual(len(result), 0)

        result = nors_utils.get_iv_antimicrobials(
            opal_models.Episode.objects.none()
        )
        self.assertEqual(len(result), 0)        

    def test_multiple_for_one_episode(self):
        today = datetime.date.today()
        antimicrobial = elcid_models.Antimicrobial(
            start_date=today - datetime.timedelta(2),
            end_date=today - datetime.timedelta(1),
            episode=self.episode,
            route_fk_id=self.iv_route.id
        )
        antimicrobial.delivered_by = self.opat_clinic.name
        antimicrobial.drug = self.fucidin.name
        antimicrobial.save()   

        antimicrobial_other = elcid_models.Antimicrobial(
            start_date=today - datetime.timedelta(2),
            end_date=today,
            episode=self.episode,
            route_fk_id=self.iv_route.id
        )
        antimicrobial_other.delivered_by = self.opat_clinic.name
        antimicrobial_other.drug = self.fucidin.name
        antimicrobial.route = "other"
        antimicrobial_other.save() 
        result = nors_utils.get_iv_antimicrobials(
            opal_models.Episode.objects.filter(id=self.episode.id)
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0]["episode_id"], self.episode.id
        )

        self.assertEqual(
            result[0]["max_end"], today
        )

    def test_multiple_episodes(self):
        today = datetime.date.today()
        antimicrobial = elcid_models.Antimicrobial(
            start_date=today - datetime.timedelta(2),
            end_date=today - datetime.timedelta(1),
            episode=self.episode,
            route_fk_id=self.iv_route.id
        )
        antimicrobial.delivered_by = self.opat_clinic.name
        antimicrobial.drug = self.fucidin.name
        antimicrobial.save()   
        _, episode_2 = self.new_patient_and_episode_please()

        antimicrobial_other = elcid_models.Antimicrobial(
            start_date=today - datetime.timedelta(2),
            end_date=today,
            episode=episode_2,
            route_fk_id=self.iv_route.id
        )
        antimicrobial_other.delivered_by = self.opat_clinic.name
        antimicrobial_other.drug = self.fucidin.name
        antimicrobial.route = "other"
        antimicrobial_other.save() 
        result = nors_utils.get_iv_antimicrobials(
            opal_models.Episode.objects.filter(id__in=[self.episode.id, episode_2.id])
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(
            result[0]["episode_id"], self.episode.id
        )

        self.assertEqual(
            result[0]["max_end"], today - datetime.timedelta(1)
        )

        self.assertEqual(
            result[1]["episode_id"], episode_2.id
        )

        self.assertEqual(
            result[1]["max_end"], today
        )


class GetNumEpisodesRejectedTestCase(OpalTestCase):
    def setUp(self):
        super(GetNumEpisodesRejectedTestCase, self).setUp()
        self.quarter = quarter_utils.Quarter(
            2018, 4
        )
        _, self.episode = self.new_patient_and_episode_please()


    def test_num_episodes_rejected_none(self):
        self.assertEqual(
            nors_utils.get_num_episodes_rejected(self.quarter),
            0
        )

    def test_num_episodes_rejected_some(self):
        opat_models.OPATRejection.objects.create(
            date=datetime.date(2018, 12, 1),
            episode=self.episode
        )
        self.assertEqual(
            nors_utils.get_num_episodes_rejected(self.quarter),
            1
        )


class IsDuplicateTestCase(OpalTestCase):
    def setUp(self):
        _, self.episode = self.new_patient_and_episode_please()
        self.drug = opal_models.Antimicrobial.objects.create(
            name="paracetomol"
        )
        self.yesterday = datetime.date.today() - datetime.timedelta(1)
        self.today = datetime.date.today()

    def test_is_duplicate_with_duplicate(self):
        antimicrobial = elcid_models.Antimicrobial.objects.create(
            episode=self.episode,
            drug_fk_id=self.drug.id,
            start_date=self.yesterday,
        )

        elcid_models.Antimicrobial.objects.create(
            episode=self.episode,
            drug_fk_id=self.drug.id,
            start_date=self.yesterday,
        )
        self.assertTrue(
            nors_utils.is_duplicate(antimicrobial)
        )

    def test_is_duplicate_without_dupliate(self):
        antimicrobial = elcid_models.Antimicrobial.objects.create(
            episode=self.episode,
            drug_fk_id=self.drug.id,
            start_date=self.today,
        )

        elcid_models.Antimicrobial.objects.create(
            episode=self.episode,
            drug_fk_id=self.drug.id,
            start_date=self.yesterday,
        )
        self.assertFalse(
            nors_utils.is_duplicate(antimicrobial)
        )

    def test_is_duplicate_with_duplicate_inpatient(self):
        antimicrobial_1 = elcid_models.Antimicrobial.objects.create(
            episode=self.episode,
            drug_fk_id=self.drug.id,
            start_date=self.yesterday,
        )

        antimicrobial_1.delivered_by = nors_utils.INPATIENT_TEAM
        antimicrobial_1.save()

        antimicrobial_2 = elcid_models.Antimicrobial.objects.create(
            episode=self.episode,
            drug_fk_id=self.drug.id,
            start_date=self.yesterday,
        )

        antimicrobial_2.delivered_by = nors_utils.INPATIENT_TEAM
        antimicrobial_2.save()
        self.assertTrue(
            nors_utils.is_duplicate(antimicrobial_1)
        )