from datetime import date

from opal.core.test import OpalTestCase
from opat.models import OPATRejection
from opat import reports
from mock import patch


class OpatReportTestCas(OpalTestCase):
    def setUp(self):
        self.report = reports.OpatReport()

    @patch("opat.reports.datetime")
    def test_get_reporting_periods(self, datetime):
        datetime.date.today.return_value = date(2017, 7, 2)
        _, episode = self.new_patient_and_episode_please()
        episode.set_tag_names(["opat"], None)
        episode.category_name = "opat"
        episode.save()
        OPATRejection.objects.create(
            episode=episode,
            date=date(2016, 5, 1)
        )
        reporting_periods = [i for i in self.report.get_reporting_periods()]
        expected = [
            {
                'reporting_period': '2017_2',
                'display_name': '2 April-June 2017',
                'year': 2017
            },
            {
                'reporting_period': '2017_1',
                'display_name': '1 January-March 2017',
                'year': 2017
            },
            {
                'reporting_period': '2016_4',
                'display_name': '4 October-December 2016',
                'year': 2016
            },
            {
                'reporting_period': '2016_3',
                'display_name': '3 July-September 2016',
                'year': 2016
            },
            {
                'reporting_period': '2016_2',
                'display_name': '2 April-June 2016',
                'year': 2016
            }
        ]
        self.assertEqual(reporting_periods, expected)
