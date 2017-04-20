import datetime
import ffs
import pytz
from mock import patch

from django.conf import settings
from django.test import TestCase, override_settings
from django.contrib.contenttypes.models import ContentType
from opal.core import exceptions
from opal.core.test import OpalTestCase
from opal.models import Patient, Episode, Condition, Synonym, Symptom
from elcid.models import (
    Location, PresentingComplaint, Result, Allergies, Demographics
)

HERE = ffs.Path.here()
TEST_DATA = HERE/'test_data'


class AbstractPatientTestCase(TestCase):
    def setUp(self):
        super(AbstractPatientTestCase, self).setUp()
        self.patient = Patient()
        self.patient.save()
        self.patient.demographics_set.update(
            consistency_token="12345678",
            first_name="John",
            surname="Smith",
            hospital_number="AA1111",
            date_of_birth="1972-06-20",
        )
        self.demographics = self.patient.demographics_set.get()


class AbstractEpisodeTestCase(AbstractPatientTestCase):
    def setUp(self):
        super(AbstractEpisodeTestCase, self).setUp()
        self.episode = Episode.objects.create(
            patient=self.patient,
            consistency_token="12345675"
        )


class DemographicsTest(OpalTestCase, AbstractPatientTestCase):

    def test_to_dict(self):
        expected_data = {
            'consistency_token': '12345678',
            'patient_id': self.patient.id,
            'id': self.demographics.id,
            'first_name': 'John',
            'surname': 'Smith',
            'middle_name': None,
            'title': '',
            'marital_status': u'',
            'religion': None,
            'created': None,
            'updated': None,
            'created_by_id': None,
            'updated_by_id': None,
            'date_of_birth': datetime.date(1972, 6, 20),
            'birth_place': '',
            'ethnicity': u'',
            'sex': '',
            'hospital_number': 'AA1111',
            'nhs_number': None,
            'date_of_death': None,
            'death_indicator': False,
            'post_code': None,
            'gp_practice_code': None,
            'external_system': None,
            'external_identifier': None
        }

        self.assertEqual(expected_data, self.demographics.to_dict(self.user))

    def test_update_from_dict(self):
        data = {
            'consistency_token': '12345678',
            'id': self.demographics.id,
            'first_name': 'Johann',
            'surname': 'Schmidt',
            'date_of_birth': '21/6/1972',
            'hospital_number': 'AA1112',
            }
        self.demographics.update_from_dict(data, self.user)
        demographics = self.patient.demographics_set.get()

        self.assertEqual('Johann', demographics.first_name)
        self.assertEqual('Schmidt', demographics.surname)
        self.assertEqual(datetime.date(1972, 6, 21), demographics.date_of_birth)
        self.assertEqual('AA1112', demographics.hospital_number)

    def test_update_from_dict_with_missing_consistency_token(self):
        with self.assertRaises(exceptions.APIError):
            self.demographics.update_from_dict({}, self.user)

    def test_update_from_dict_with_incorrect_consistency_token(self):
        with self.assertRaises(exceptions.ConsistencyError):
            self.demographics.update_from_dict({'consistency_token': '87654321'}, self.user)

    @override_settings(GLOSS_ENABLED=True)
    @patch("opal.models.Subrecord.get_form_template")
    def test_get_demographics_form_with_gloss(self, form_template_mock):
        form_template_mock.return_value = "some_template.html"
        form_template = Demographics.get_form_template()
        self.assertEqual(form_template, "some_template.html")

    @override_settings(GLOSS_ENABLED=False)
    def test_get_demographics_form_without_gloss(self):
        form_template = Demographics.get_form_template()
        self.assertEqual(
            form_template, "forms/demographics_form_pre_gloss.html"
        )


class LocationTest(OpalTestCase, AbstractEpisodeTestCase):

    def setUp(self):
        super(LocationTest, self).setUp()

        self.location = Location.objects.create(
            bed="13",
            category="Inpatient",
            consistency_token="12345678",
            hospital="UCH",
            ward="T10",
            episode=self.episode
        )

    def test_to_dict(self):
        expected_data = {
            'consistency_token': '12345678',
            'episode_id': self.episode.id,
            'id': self.location.id,
            'category': 'Inpatient',
            'hospital': 'UCH',
            'ward': 'T10',
            'bed': '13',
            'created': None,
            'updated': None,
            'updated_by_id': None,
            'created_by_id': None,
            'opat_acceptance': None,
            'opat_discharge': None,
            'opat_referral': None,
            'opat_referral_route': None,
            'opat_referral_team': None,
            'opat_referral_consultant': None,
            'opat_referral_team_address': None,
            }
        result = {str(k): v for k, v in self.location.to_dict(self.user).iteritems()}
        self.assertEqual(expected_data, result)

    def test_update_from_dict(self):
        data = {
            'consistency_token': '12345678',
            'id': self.location.id,
            'category': 'Inpatient',
            'hospital': 'HH',
            'ward': 'T10',
            'bed': '13',
            }
        self.location.update_from_dict(data, self.user)
        self.assertEqual('HH', self.location.hospital)


class PresentingComplaintTest(OpalTestCase, AbstractEpisodeTestCase):
    def setUp(self):
        super(PresentingComplaintTest, self).setUp()
        self.symptom_1 = Symptom.objects.create(name="tiredness")

        synonym_content_type = ContentType.objects.get_for_model(
            Symptom
        )

        self.synonym_1 = Synonym.objects.get_or_create(
            content_type=synonym_content_type,
            object_id=self.symptom_1.id,
            name="drowsy"
        )

        self.symptom_2 = Symptom.objects.create(name="alertness")
        self.symptom_3 = Symptom.objects.create(name="apathy")
        self.presenting_complaint = PresentingComplaint.objects.create(
            symptom=self.symptom_1,
            duration="a week",
            details="information",
            consistency_token=1111,
            episode=self.episode
        )
        self.presenting_complaint.symptoms.add(self.symptom_2, self.symptom_3)

    def test_to_dict(self):
        expected_data = dict(
            id=self.presenting_complaint.id,
            consistency_token=self.presenting_complaint.consistency_token,
            symptoms=["alertness", "apathy"],
            duration="a week",
            details="information",
            episode_id=1,
            updated=None,
            updated_by_id=None,
            created=None,
            created_by_id=None
        )
        self.assertEqual(
            expected_data, self.presenting_complaint.to_dict(self.user)
        )

    def test_do_dict_with_fields(self):
        expected_data = dict(id=self.presenting_complaint.id)
        self.assertEqual(
            expected_data,
            self.presenting_complaint.to_dict(self.user, fields=["id"])
        )

    def test_update_from_dict(self):
        data = {
            u'consistency_token': self.presenting_complaint.consistency_token,
            u'id': self.presenting_complaint.id,
            u'symptoms': [u'alertness', u'tiredness'],
            u'duration': 'a month',
            u'details': 'other information'
        }
        self.presenting_complaint.update_from_dict(data, self.user)
        new_symptoms = self.presenting_complaint.symptoms.values_list(
            "name", flat=True
        )
        self.assertEqual(set(new_symptoms), set([u'alertness', u'tiredness']))
        self.assertEqual(self.presenting_complaint.duration, 'a month')
        self.assertEqual(
            self.presenting_complaint.details, 'other information'
        )

    def test_update_from_dict_with_synonymns(self):
        data = {
            u'consistency_token': self.presenting_complaint.consistency_token,
            u'id': self.presenting_complaint.id,
            u'symptoms': [u'alertness', u'drowsy'],
            u'duration': 'a month',
            u'details': 'other information'
        }
        self.presenting_complaint.update_from_dict(data, self.user)
        new_symptoms = self.presenting_complaint.symptoms.values_list(
            "name", flat=True
        )
        self.assertEqual(set(new_symptoms), set([u'alertness', u'tiredness']))
        self.assertEqual(self.presenting_complaint.duration, 'a month')
        self.assertEqual(
            self.presenting_complaint.details, 'other information'
        )


    def test_update_with_dict_synonyms_new_complaint(self):
        data = {
            'episode_id': self.episode.id,
            u'symptoms': [u'alertness', u'drowsy'],
            u'duration': 'a month',
            u'details': 'other information'
        }
        presenting_complaint = PresentingComplaint()
        presenting_complaint.update_from_dict(data, self.user)
        new_symptoms = presenting_complaint.symptoms.values_list(
            "name", flat=True
        )
        self.assertEqual(set(new_symptoms), set([u'alertness', u'tiredness']))
        self.assertEqual(presenting_complaint.duration, 'a month')
        self.assertEqual(
            presenting_complaint.details, 'other information'
        )


class ResultTest(OpalTestCase, AbstractPatientTestCase):
    def test_to_dict_and_from_dict(self):
        datetime_format = settings.DATETIME_INPUT_FORMATS[0]

        request_datetime = datetime.datetime(2016, 1, 2).strftime(
            datetime_format
        )
        observation_datetime = datetime.datetime(2016, 1, 6).strftime(
            datetime_format
        )
        last_edited = datetime.datetime(2016, 1, 7).strftime(
            datetime_format
        )

        result_args = dict(
            patient_id=self.patient.id,
            lab_number="234324",
            profile_code="2343344",
            external_identifier="234324.2343344",
            profile_description="RENAL PROFILE",
            request_datetime=request_datetime,
            observation_datetime=observation_datetime,
            last_edited=last_edited,
            result_status="FINAL",
            observations=[{
                u'comments': None,
                u'observation_value': u'250',
                u'reference_range': u'150-400',
                u'result_status': None,
                u'test_code': u'PLT',
                u'test_name': u'Platelet count',
                u'units': u'x10^9/L',
                u'value_type': u'NM'
            }, {
                u'comments': None,
                u'observation_value': u'10.0',
                u'reference_range': u'7-13',
                u'result_status': None,
                u'test_code': u'MPVU',
                u'test_name': u'MPV',
                u'units': u'fL',
                u'value_type': u'NM'
            }]
        )

        result = Result()
        result.update_from_dict(result_args, self.user)

        found_result = Result.objects.get()
        self.assertEqual(found_result.lab_number, "234324")
        self.assertEqual(found_result.profile_code, "2343344")

        back_to_dict = found_result.to_dict(self.user)
        del back_to_dict["updated"]
        del back_to_dict["updated_by_id"]
        del back_to_dict["created"]
        del back_to_dict["created_by_id"]
        del back_to_dict["consistency_token"]
        del back_to_dict["id"]
        result_args["request_datetime"] = datetime.datetime(
            2016, 1, 2, tzinfo=pytz.UTC
        )
        result_args["observation_datetime"] = datetime.datetime(
            2016, 1, 6, tzinfo=pytz.UTC
        )
        result_args["last_edited"] = datetime.datetime(
            2016, 1, 7, tzinfo=pytz.UTC
        )

        self.assertEqual(result_args, back_to_dict)

    def test_updates_with_external_identifer(self):
        Result.objects.create(
            result_status="Incomplete",
            external_identifier="1",
            patient=self.patient
        )

        update_dict = dict(
            result_status="Complete",
            external_identifier="1",
            patient_id=self.patient.id
        )

        a = Result()
        a.update_from_dict(update_dict, self.user)

        result = Result.objects.get()
        self.assertEqual(
            result.result_status, "Complete"
        )

    def test_no_external_identifier(self):
        Result.objects.create(
            result_status="Incomplete",
            external_identifier="1",
            patient=self.patient
        )

        update_dict = dict(
            result_status="Complete",
            patient_id=self.patient.id
        )

        a = Result()
        a.update_from_dict(update_dict, self.user)
        results = Result.objects.all()
        self.assertEqual(2, len(results))
        self.assertEqual(
            results[0].result_status, "Incomplete"
        )
        self.assertEqual(
            results[1].result_status, "Complete"
        )
        self.assertEqual(
            results[1].external_identifier, None
        )

    def test_doesnt_update_empty_external_identifier(self):
        Result.objects.create(
            result_status="Incomplete",
            external_identifier="",
            patient=self.patient
        )

        update_dict = dict(
            result_status="Complete",
            external_identifier="",
            patient_id=self.patient.id
        )

        a = Result()
        a.update_from_dict(update_dict, self.user)
        results = Result.objects.all()
        self.assertEqual(2, len(results))
        self.assertEqual(
            results[0].result_status, "Incomplete"
        )
        self.assertEqual(
            results[1].result_status, "Complete"
        )

    def test_next_updates_a_different_patient(self):
        other_patient = Patient.objects.create()
        Result.objects.create(
            result_status="Incomplete",
            external_identifier="1",
            patient=self.patient
        )

        update_dict = dict(
            result_status="Complete",
            external_identifier="1",
            patient_id=other_patient.id
        )

        a = Result()
        a.update_from_dict(update_dict, self.user)
        results = Result.objects.all()
        self.assertEqual(2, len(results))
        self.assertEqual(
            results[0].patient, self.patient
        )
        self.assertEqual(
            results[1].patient, other_patient
        )


class AllergyTest(OpalTestCase):
    def test_get_modal_footer_template(self):
        self.assertEqual(
            Allergies.get_modal_footer_template(),
            "partials/_sourced_modal_footer.html"
        )


class DiagnosisTest(OpalTestCase, AbstractEpisodeTestCase):

    def setUp(self):
        super(DiagnosisTest, self).setUp()
        self.condition_1 = Condition.objects.create(name="Some condition")
        self.condition_2 = Condition.objects.create(name="Some other condition")
        Synonym.objects.create(
            name="Condition synonym",
            content_object=self.condition_2
        )

        self.diagnosis = self.episode.diagnosis_set.create(
            consistency_token="12345678",
            date_of_diagnosis=datetime.date(2013, 7, 25),
            details="",
            provisional=False,
            condition=self.condition_1.name,
        )

        self.episode.diagnosis_set.create(
            condition=self.condition_2.name,
            date_of_diagnosis=datetime.date(2013, 7, 25),
            details="",
            provisional=True,
        )

        self.diagnosis = self.episode.diagnosis_set.first()

    def test_to_dict(self):
        expected_data = {
            'consistency_token': u'12345678',
            'updated': None,
            'created': None,
            'updated_by_id': None,
            'created_by_id': None,
            'episode_id': self.episode.id,
            'id': self.diagnosis.id,
            'condition': 'Some condition',
            'provisional': False,
            'details': u'',
            'date_of_diagnosis': datetime.date(2013, 7, 25),
            }

        result = {str(k): v for k, v in self.diagnosis.to_dict(self.user).iteritems()}
        self.assertEqual(expected_data, result)

    def test_update_from_dict_with_existing_condition(self):
        data = {
            'consistency_token': '12345678',
            'id': self.diagnosis.id,
            'condition': 'Some other condition',
            }
        self.diagnosis.update_from_dict(data, self.user)
        diagnosis = self.episode.diagnosis_set.first()
        self.assertEqual('Some other condition', diagnosis.condition)

    def test_update_from_dict_with_synonym_for_condition(self):
        data = {
            'consistency_token': '12345678',
            'id': self.diagnosis.id,
            'condition': 'Condition synonym',
            }
        self.diagnosis.update_from_dict(data, self.user)
        diagnosis = self.episode.diagnosis_set.first()
        self.assertEqual('Some other condition', diagnosis.condition)

    def test_update_from_dict_with_new_condition(self):
        data = {
            'consistency_token': '12345678',
            'id': self.diagnosis.id,
            'condition': 'New condition',
            }
        self.diagnosis.update_from_dict(data, self.user)
        diagnosis = self.episode.diagnosis_set.first()
        self.assertEqual('New condition', diagnosis.condition)


@patch("elcid.gloss_api.subscribe")
@patch("elcid.gloss_api.patient_query")
class TestGlossUpdate(AbstractPatientTestCase):
    @override_settings(GLOSS_ENABLED=True)
    def test_with_settings_on_create(self, patient_query, subscribe):
        episode = self.patient.create_episode()
        subscribe.assert_called_once_with("AA1111")
        patient_query.assert_called_once_with("AA1111", episode=episode)

    def test_not_called_on_update(self, patient_query, subscribe):
        with override_settings(GLOSS_ENABLED=False):
            episode = self.patient.create_episode()

        with override_settings(GLOSS_ENABLED=True):
            episode.save()

        self.assertFalse(patient_query.called)
        self.assertFalse(subscribe.called)

    @override_settings(GLOSS_ENABLED=False)
    def test_without_settings_enabled(self, patient_query, subscribe):
        self.patient.create_episode()
        self.assertFalse(patient_query.called)
        self.assertFalse(subscribe.called)
