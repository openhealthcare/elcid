from datetime import date

from opal.core.test import OpalTestCase
from opat import reports
from mock import patch


class OpatReportTestCase(OpalTestCase):
    def setUp(self):
        self.report = reports.OpatReport()

    def test_get_date_range_from_reporting_period(self):
        # beginning of the year
        expected = date(2015, 1, 1), date(2015, 4, 1)
        found = self.report.get_date_range_from_reporting_period("2015_1")
        self.assertEqual(expected, found)

        # middle of the year
        expected = date(2015, 7, 1), date(2015, 10, 1)
        found = self.report.get_date_range_from_reporting_period("2015_3")
        self.assertEqual(expected, found)

        # end of the year
        expected = date(2015, 10, 1), date(2016, 1, 1)
        found = self.report.get_date_range_from_reporting_period("2015_4")
        self.assertEqual(expected, found)

    @patch("opat.reports.datetime")
    def test_get_reporting_periods(self, datetime):
        datetime.date.today.return_value = date(2017, 7, 2)
        _, episode = self.new_patient_and_episode_please()
        episode.set_tag_names(["opat"], None)
        episode.category_name = "opat"
        episode.save()
        location = episode.location_set.get()
        location.opat_acceptance = date(2016, 5, 1)
        location.save()

        reporting_periods = [i for i in self.report.get_reporting_periods()]
        expected = [
            {
                'reporting_period': '2017_2',
                'display_name': 'Apr - Jun 2017',
                'year': 2017
            },
            {
                'reporting_period': '2017_1',
                'display_name': 'Jan - Mar 2017',
                'year': 2017
            },
            {
                'reporting_period': '2016_4',
                'display_name': 'Oct - Dec 2016',
                'year': 2016
            },
            {
                'reporting_period': '2016_3',
                'display_name': 'Jul - Sep 2016',
                'year': 2016
            },
            {
                'reporting_period': '2016_2',
                'display_name': 'Apr - Jun 2016',
                'year': 2016
            }
        ]
        self.assertEqual(reporting_periods, expected)
