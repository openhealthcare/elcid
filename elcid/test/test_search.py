from mock import patch

from opal.core.test import OpalTestCase
from opal.core.search import queries
from opal import models as omodels


@patch("elcid.search.requests.get")
class SearchTestCase(OpalTestCase):
    expected_gloss_result = {
        'first_name': 'Jane',
        'surname': 'Smith',
        'middle_name': None,
        'title': 'Ms',
        'gp_practice_code': None,
        'post_code': None,
        'ethnicity': None,
        'sex': None,
        'marital_status': None,
        'death_indicator': False,
        'date_of_birth': '12/12/1983',
        'date_of_death': None,
    }

    def test_gloss_query_flow(self, requests_mock):
        criteria = [{
            "queryType": "Equals",
            "query": "1231111",
            "field": "Hospital Number",
            'combine': 'and',
            'column': u'demographics',
        }]
        queries.create_query(self.user, criteria)
        self.assertFalse(omodels.Patient.objects.exists())

    def test_database_flow(self, requests_mock):
        pass
