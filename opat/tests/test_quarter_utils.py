import mock
import datetime
from opal.core.test import OpalTestCase
from opat import quarter_utils


class QuarterUtilsTestCase(OpalTestCase):

    @mock.patch('opat.quarter_utils.datetime')
    def test_get_previous_quarters(self, dt):
        dt.date.today.return_value = datetime.date(2018, 9, 3)
        dt.date.side_effect = datetime.date
        result = quarter_utils.get_previous_quarters(2)
        self.assertEqual(
            result,
            [
                quarter_utils.Quarter(2018, 2),
                quarter_utils.Quarter(2018, 1)
            ]
        )

    def test_eq(self):
        q = quarter_utils.Quarter(2018, 1)
        p = quarter_utils.Quarter(2018, 1)
        self.assertEqual(p, q)

        r = quarter_utils.Quarter(2018, 2)
        self.assertNotEqual(r, q)

    def test_hash(self):
        q = quarter_utils.Quarter(2018, 1)
        p = quarter_utils.Quarter(2018, 1)
        d = {q: True}
        self.assertTrue(d[p])
        r = quarter_utils.Quarter(2018, 2)
        self.assertFalse(d.get(r, False))

    def test_cmp(self):
        year_before = quarter_utils.Quarter(2017, 3)
        period_before = quarter_utils.Quarter(2017, 1)
        main_quarter = quarter_utils.Quarter(2018, 2)
        same_quarter = quarter_utils.Quarter(2018, 2)

        self.assertTrue(year_before < main_quarter)
        self.assertTrue(period_before < main_quarter)
        self.assertFalse(same_quarter < main_quarter)
        self.assertFalse(main_quarter < same_quarter)

    def test_get_start_end_from_quarter(self):
        self.assertEqual(
            quarter_utils.get_start_end_from_quarter(2018, 1),
            (datetime.date(2018, 1, 1), datetime.date(2018, 3, 31),)
        )

        self.assertEqual(
            quarter_utils.get_start_end_from_quarter(2018, 2),
            (datetime.date(2018, 4, 1), datetime.date(2018, 6, 30),)
        )

        self.assertEqual(
            quarter_utils.get_start_end_from_quarter(2018, 3),
            (datetime.date(2018, 7, 1), datetime.date(2018, 9, 30),)
        )

        self.assertEqual(
            quarter_utils.get_start_end_from_quarter(2018, 4),
            (datetime.date(2018, 10, 1), datetime.date(2018, 12, 31),)
        )
