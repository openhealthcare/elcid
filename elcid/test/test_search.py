from mock import patch, MagicMock
from copy import copy
import json

from opal.core.test import OpalTestCase
from opal.core.search import queries
from opal import models as omodels


@patch("elcid.gloss_api.requests.get")
class SearchTestCase(OpalTestCase):
    returned_gloss_result = {
        'demographics': [{
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
        }],
        'duplicate_patient': []
    }

    criteria = [{
        "queryType": "Equals",
        "query": "1231111",
        "field": "Hospital Number",
        'combine': 'and',
        'column': u'demographics',
    }]

    def test_recusive_gloss_search(self, requests_mock):
        return_1 = copy(self.returned_gloss_result)
        return_1["duplicate_patient"] = [dict(new_id="1000")]

        return_2 = copy(self.returned_gloss_result)
        return_2["duplicate_patient"] = [dict(new_id="1001")]
        return_2["demographics"][0]["first_name"] = "Sue"
        return_2["demographics"][0]["hospital_number"] = "1000"

        return_3 = copy(self.returned_gloss_result)
        return_3["demographics"][0]["first_name"] = "Sarah"
        return_3["demographics"][0]["hospital_number"] = "1001"

        side_effects = []

        for result in [return_1, return_2, return_3]:
            response = MagicMock()
            response.content = json.dumps({
                "status": "success",
                "messages": result
            })
            side_effects.append(response)

        requests_mock.side_effect = side_effects
        query = queries.create_query(self.user, self.criteria)
        result = query.patients_as_json()[0]
        self.assertEqual(requests_mock.call_count, 3)
        merged = [{
            'duplicate_patient': [],
            'demographics': [{
                'first_name': u'Sarah',
                'post_code': None,
                'surname': u'Smith',
                'gp_practice_code': None,
                'title': u'Ms',
                'hospital_number': 1001,
                'marital_status': None,
                'date_of_death': None,
                'sex': None,
                'date_of_birth': u'12/12/1983',
                'death_indicator': False,
                'sourced_from_upstream': True,
                'middle_name': None,
                'hospital_number': "1001",
                'ethnicity': None}]
        }]

        expected = copy(self.returned_gloss_result)
        expected["demographics"][0]['sourced_from_upstream'] = True
        expected["demographics"][0]['hospital_number'] = "1231111"
        expected["duplicate_patient"] = [{u'new_id': "1001"}]
        expected["merged"] = merged
        self.assertEqual(result, expected)

    def test_gloss_query_flow(self, requests_mock):
        requests_mock.return_value = MagicMock()
        requests_mock.return_value.content = json.dumps({
            "status": "success",
            "messages": self.returned_gloss_result
        })
        self.assertFalse(omodels.Patient.objects.exists())

        query = queries.create_query(self.user, self.criteria)
        result = query.patients_as_json()[0]

        expected = copy(self.returned_gloss_result)
        expected["demographics"][0]["sourced_from_upstream"] = True
        expected["demographics"][0]["hospital_number"] = "1231111"
        self.assertEqual(result, expected)
        requests_mock.assert_called_once_with(
            "http://0.0.0.0:6767/api/demographics/1231111"
        )

    def test_database_flow(self, requests_mock):
        patient = omodels.Patient.objects.create()
        patient.create_episode()
        demographics = patient.demographics_set.first()
        demographics.hospital_number = "1231111"
        demographics.first_name = "Sue"
        demographics.save()
        query = queries.create_query(self.user, self.criteria)
        result = query.patients_as_json()[0]
        self.assertEqual(result["demographics"][0]["first_name"], "Sue")
        self.assertFalse(requests_mock.called)
