import datetime
from dateutil.relativedelta import relativedelta
from mock import patch

from opal.core.test import OpalTestCase
from opal.models import Episode

from infectiousdiseases.reports import IdLiasionReport


class IdLiasionReportTestCase(OpalTestCase):
    def setUp(self):
        self.report = IdLiasionReport()

    def test_get_queryset_vanilla(self):
        _, e1 = self.new_patient_and_episode_please()
        e1.end = datetime.date(2017, 5, 5)
        e1.tagging_set.create(
            value="id_liaison",
            archived=True,
        )
        e1.save()

        _, e2 = self.new_patient_and_episode_please()
        e2.end = datetime.date(2017, 5, 5)

        e2.tagging_set.create(
            value="something_else",
            archived=True,
        )
        e2.save()
        result = self.report.get_queryset(datetime.date(2017, 5, 1))
        self.assertEqual(
            list(result), list(Episode.objects.filter(id=e1.id))
        )

    def test_get_queryset_tagging_archived(self):
        _, e1 = self.new_patient_and_episode_please()
        e1.end = datetime.date(2017, 5, 5)
        e1.save()
        e1.tagging_set.create(
            value="id_liaison",
            archived=False,
        )
        e1.tagging_set.create(
            value="else",
            archived=True,
        )
        result = self.report.get_queryset(datetime.date(2017, 5, 1))
        self.assertFalse(result.exists())

    @patch("infectiousdiseases.reports.datetime")
    def test_get_age_earlier_year(self, dt):
        dt.date.today.return_value = datetime.date(2017, 4, 5)
        patient, _ = self.new_patient_and_episode_please()
        demographics = patient.demographics_set.first()
        demographics.date_of_birth = datetime.date(2010, 5, 1)

        self.assertEqual(
            self.report.get_age(demographics), 6
        )

    @patch("infectiousdiseases.reports.datetime")
    def test_get_age_later_year(self, dt):
        dt.date.today.return_value = datetime.date(2017, 6, 5)
        patient, _ = self.new_patient_and_episode_please()
        demographics = patient.demographics_set.first()
        demographics.date_of_birth = datetime.date(2010, 5, 1)
        demographics.save()

        self.assertEqual(
            self.report.get_age(demographics), 7
        )

    def test_get_age_unkown(self):
        patient, _ = self.new_patient_and_episode_please()
        demographics = patient.demographics_set.first()

        self.assertEqual(
            self.report.get_age(demographics), ""
        )

    def test_get_demographics_row(self):
        patient, episode = self.new_patient_and_episode_please()
        patient.demographics_set.update(
            first_name="Sandra",
            surname="Wallis",
            date_of_birth=datetime.date(2010, 5, 1),
            sex_ft=""
        )
        self.assertEqual(
            self.report.get_demographics_row(episode),
            ["Sandra Wallis", 7, ""]
        )

    def test_get_demographics_headers(self):
        qs = Episode.objects.none()
        self.report.qs = qs
        self.assertEqual(
            self.report.get_demographics_headers(),
            ["Name", "Age", "Gender"]
        )

    def test_get_diagnosis_repititions(self):
        _, episode = self.new_patient_and_episode_please()
        episode.diagnosis_set.create(
            condition_ft="something"
        )
        episode.diagnosis_set.create(
            condition_ft="something-else"
        )
        _, episode_2 = self.new_patient_and_episode_please()
        episode_2.diagnosis_set.create(
            condition_ft="something"
        )
        self.report.qs = Episode.objects.all()
        self.assertEqual(
            self.report.diagnosis_repetitions,
            2
        )

    def test_get_diagnosis_headers(self):
        _, episode = self.new_patient_and_episode_please()
        episode.diagnosis_set.create(
            condition_ft="something"
        )
        episode.diagnosis_set.create(
            condition_ft="something-else"
        )
        _, episode_2 = self.new_patient_and_episode_please()
        episode_2.diagnosis_set.create(
            condition_ft="something"
        )
        self.report.qs = Episode.objects.all()
        self.assertEqual(
            self.report.diagnosis_repetitions,
            2
        )
        self.report.qs = Episode.objects.all()
        self.assertEqual(
            self.report.get_diagnosis_headers(),
            ['Condition 1', 'Condition 2']
        )

    def test_get_diagnosis_row(self):
        _, episode = self.new_patient_and_episode_please()
        episode.diagnosis_set.create(
            condition_ft="something"
        )
        episode.diagnosis_set.create(
            condition_ft="something-else"
        )
        _, episode_2 = self.new_patient_and_episode_please()
        episode_2.diagnosis_set.create(
            condition_ft="something"
        )
        self.report.qs = Episode.objects.all()
        self.assertEqual(
            self.report.diagnosis_repetitions,
            2
        )
        self.report.qs = Episode.objects.all()
        self.assertEqual(
            self.report.get_diagnosis_row(episode),
            ['something', 'something-else']
        )
        self.assertEqual(
            self.report.get_diagnosis_row(episode_2),
            ['something', '']
        )

    def test_get_clinical_advice_headers(self):
        self.assertEqual(
            self.report.get_clinical_advice_headers(),
            [
                "Clinical Advice Given",
                "Infection Control Advice Given",
                "Change In Antibiotic Prescription",
                "Referred To Opat"
            ]
        )

    def test_get_clinical_advice_none(self):
        _, episode = self.new_patient_and_episode_please()
        self.assertEqual(
            self.report.get_clinical_advice_row(episode),
            [0, 0, 0, 0]
        )

    def test_get_clinical_advice_row_empty(self):
        _, episode = self.new_patient_and_episode_please()
        episode.microbiologyinput_set.create()
        self.assertEqual(
            self.report.get_clinical_advice_row(episode),
            [0, 0, 0, 0]
        )

    def test_get_clinical_advice_row_aggregate(self):
        _, episode = self.new_patient_and_episode_please()
        episode.microbiologyinput_set.create()
        episode.microbiologyinput_set.create(
            clinical_advice_given=True
        )
        episode.microbiologyinput_set.create(
            clinical_advice_given=True
        )
        self.assertEqual(
            self.report.get_clinical_advice_row(episode),
            [2, 0, 0, 0]
        )

    def test_infectious_advice_given(self):
        _, episode = self.new_patient_and_episode_please()
        episode.microbiologyinput_set.create()
        episode.microbiologyinput_set.create(
            infection_control_advice_given=True
        )

        self.assertEqual(
            self.report.get_clinical_advice_row(episode),
            [0, 1, 0, 0]
        )

    def test_change_in_antibiotic_prescription_given(self):
        _, episode = self.new_patient_and_episode_please()
        episode.microbiologyinput_set.create()
        episode.microbiologyinput_set.create(
            change_in_antibiotic_prescription=True
        )

        self.assertEqual(
            self.report.get_clinical_advice_row(episode),
            [0, 0, 1, 0]
        )

    def test_change_in_referred_to_opat_given(self):
        _, episode = self.new_patient_and_episode_please()
        episode.microbiologyinput_set.create()
        episode.microbiologyinput_set.create(
            referred_to_opat=True
        )

        self.assertEqual(
            self.report.get_clinical_advice_row(episode),
            [0, 0, 0, 1]
        )

    def test_empty_report(self):
        report = self.report.generate_report_data(
            criteria=dict(reporting_month="01/05/2017")
        )
        # we just return headers
        self.assertEqual(
            report[0].file_data[0],
            [
                'Name',
                'Age',
                'Gender',
                'Clinical Advice Given',
                'Infection Control Advice Given',
                'Change In Antibiotic Prescription',
                'Referred To Opat'
            ]
        )

    def test_generate_report_data(self):
        patient, episode = self.new_patient_and_episode_please()
        patient_2, episode_2 = self.new_patient_and_episode_please()
        episode.end = datetime.date(2017, 5, 5)
        episode.tagging_set.create(
            value="id_liaison",
            archived=True,
        )
        episode.save()

        episode_2.end = datetime.date(2017, 5, 5)

        episode_2.tagging_set.create(
            value="id_liaison",
            archived=True,
        )
        episode_2.save()

        patient.demographics_set.update(
            first_name="Sandra",
            surname="Wallis",
            date_of_birth=datetime.date(2010, 5, 1),
            sex_ft="Unknown"
        )

        patient_2.demographics_set.update(
            first_name="Gemma",
            surname="Potts",
            date_of_birth=datetime.date(2000, 5, 1),
            sex_ft="Female"
        )

        episode.diagnosis_set.create(
            condition_ft="something"
        )

        episode.diagnosis_set.create(
            condition_ft="something-else"
        )
        episode_2.diagnosis_set.create(
            condition_ft="something"
        )

        reports = self.report.generate_report_data(
            criteria=dict(reporting_month="01/05/2017")
        )

        self.assertEqual(len(reports), 1)

        report = reports[0]

        self.assertEqual(report.file_name, "id_liasion_report_5_2017.csv")
        self.assertEqual(
            report.file_data[0],
            [
                'Name',
                'Age',
                'Gender',
                'Condition 1',
                'Condition 2',
                'Clinical Advice Given',
                'Infection Control Advice Given',
                'Change In Antibiotic Prescription',
                'Referred To Opat'
            ]
        )

        self.assertEqual(
            report.file_data[1],
            [
                'Sandra Wallis',
                7,
                'Unknown',
                'something',
                'something-else',
                0,
                0,
                0,
                0
            ]
        )

        self.assertEqual(
            report.file_data[2],
            [
                'Gemma Potts',
                17,
                'Female',
                'something',
                '',
                0,
                0,
                0,
                0
            ]
        )

    @patch("infectiousdiseases.reports.datetime")
    def test_report_rows_only_2(self, dt):

        # override datetime.date.today
        class NewDate(datetime.date):
            @classmethod
            def today(cls):
                return cls(2017, 7, 2)
        dt.date = NewDate
        some_date = datetime.date(2017, 05, 3)
        _, e = self.new_patient_and_episode_please()
        e.end = some_date
        e.save()
        e.tagging_set.create(
            value="id_liaison",
            archived=True,
        )
        ctx = self.report.report_rows
        self.assertEqual(
            len(ctx),
            1
        )
        self.assertEqual(
            len(ctx[0]),
            2
        )
        self.assertEqual(
            ctx[0][0],
            {
                'display_month': 'June',
                'value': '01/06/2017',
                'display_year': '2017'
            }
        )

        self.assertEqual(
            ctx[0][1],
            {
                'display_month': 'May',
                'value': '01/05/2017',
                'display_year': '2017'
            }
        )

    @patch("infectiousdiseases.reports.datetime")
    def test_report_rows_chunking(self, dt):

        # override datetime.date.today
        class NewDate(datetime.date):
            @classmethod
            def today(cls):
                return cls(2017, 7, 2)
        dt.date = NewDate
        some_date = datetime.date(2016, 5, 3)
        _, e = self.new_patient_and_episode_please()
        e.end = some_date
        e.save()
        e.tagging_set.create(
            value="id_liaison",
            archived=True,
        )
        ctx = self.report.report_rows
        self.assertEqual(
            len(ctx),
            4
        )
        self.assertEqual(
            len(ctx[3]),
            2
        )

    def test_report_rows_none(self):
        self.assertIsNone(self.report.report_rows)
