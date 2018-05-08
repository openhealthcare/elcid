"""
unittests for search.views
"""
import json
from django.core.urlresolvers import reverse
from datetime import date

from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import override_settings
from mock import patch, mock_open

from opal import models
from opal.tests import models as tmodels
from opal.core.test import OpalTestCase
from search import views, queries, extract


class BaseSearchTestCase(OpalTestCase):

    def create_patient(self, first_name, last_name, hospital_number):
        patient, episode = self.new_patient_and_episode_please()
        demographics = patient.demographics_set.get()
        demographics.first_name = first_name
        demographics.surname = last_name
        demographics.hospital_number = hospital_number
        demographics.save()
        return patient, episode

    def setUp(self):
        self.patient, self.episode = self.create_patient(
            "Sean", "Connery", "007"
        )

    def get_logged_in_request(self, url=None):
        if url is None:
            url = "/"
        request = self.rf.get(url)
        request.user = self.user
        return request

    def get_not_logged_in_request(self, url=None):
        if url is None:
            url = "/"
        request = self.rf.get(url)
        request.user = AnonymousUser()
        return request

    def get_response(self, url=None, view=None):
        request = self.get_logged_in_request(url)
        if view is None:
            view = self.view
        return self.view(request)


class PatientSearchTestCase(BaseSearchTestCase):

    def setUp(self):
        self.url = '/search/patient/'
        self.view = views.patient_search_view
        super(PatientSearchTestCase, self).setUp()

    def test_not_logged_in(self):
        request = self.get_not_logged_in_request()
        with self.assertRaises(PermissionDenied):
            self.view(request)

    # Searching for a patient that doesn't exist by Hospital Number
    def test_patient_does_not_exist_number(self):
        url = '%s?hospital_number=notareanumber' % self.url
        resp = self.get_response(url)
        data = json.loads(resp.content.decode('UTF-8'))
        self.assertEqual([], data)

    # Searching for a patient that exists by Hospital Number
    def test_patient_exists_number(self):
        url = '/search/patient/?hospital_number=007'
        resp = self.get_response(url)
        data = json.loads(resp.content.decode('UTF-8'))
        expected = [self.patient.to_dict(self.user)]

        expected = json.loads(json.dumps(expected, cls=DjangoJSONEncoder))
        self.assertEqual(expected, data)

    # TODO:
    # Searching for a patient that exists but only has episodes that are
    # restricted teams that the user is not a member of.

    def test_must_provide_hospital_number(self):
        url = "/search/patient/"
        resp = self.get_response(url)
        self.assertEqual(400, resp.status_code)


class SimpleSearchViewTestCase(BaseSearchTestCase):
    maxDiff = None

    def setUp(self):
        super(SimpleSearchViewTestCase, self).setUp()
        self.url = '/search/simple/'
        self.view = views.simple_search_view
        self.expected = {
            u'page_number': 1,
            u'object_list': [{
                u'count': 1,
                u'id': self.patient.id,
                u'first_name': u'Sean',
                u'surname': u'Connery',
                u'end': u'15/10/2015',
                u'patient_id': 1,
                u'hospital_number': u'007',
                u'date_of_birth': None,
                u'start': u'15/10/2015',
                u'categories': [u'Inpatient']
            }],
            u'total_count': 1,
            u'total_pages': 1,
        }

        self.empty_expected = {
            "page_number": 1,
            "object_list": [],
            "total_pages": 1,
            "total_count": 0
        }
        dt = date(
            day=15, month=10, year=2015
        )
        self.episode.date_of_episode = dt
        self.episode.start = dt
        self.episode.end = dt
        self.episode.save()

    def test_not_logged_in(self):
        request = self.get_not_logged_in_request()
        with self.assertRaises(PermissionDenied):
            self.view(request)

    def test_must_provide_name_or_hospital_number(self):
        resp = self.get_response(self.url)
        self.assertEqual(400, resp.status_code)

    # Searching for a patient that exists by partial name match
    def test_patient_exists_partial_name(self):
        resp = self.get_response("%s?query=Co" % self.url)
        data = json.loads(resp.content.decode('UTF-8'))
        self.assertEqual(self.expected, data)

    # Searching for a patient that exists by partial HN match
    def test_patient_exists_partial_number(self):
        resp = self.get_response('%s?query=07' % self.url)
        data = json.loads(resp.content.decode('UTF-8'))
        self.assertEqual(self.expected, data)

    # Searching for a patient that exists by name
    def test_patient_exists_name(self):
        resp = self.get_response('%s?query=Connery' % self.url)
        data = json.loads(resp.content.decode('UTF-8'))
        self.assertEqual(self.expected, data)

    # Searching for a patient that doesn't exist by Hospital Number
    def test_patient_does_not_exist_number(self):
        resp = self.get_response('%s?query=notareanumber' % self.url)
        data = json.loads(resp.content.decode('UTF-8'))
        self.assertEqual(self.empty_expected, data)

    # Searching for a patient that doesn't exist by name
    def test_patient_does_not_exist_name(self):
        request = self.rf.get('%s/?query=notareaname' % self.url)
        request.user = self.user
        resp = self.view(request)
        data = json.loads(resp.content.decode('UTF-8'))
        self.assertEqual(self.empty_expected, data)

    # Searching for a patient that exists by Hospital Number
    def test_patient_exists_number(self):
        request = self.rf.get('%s/?query=007' % self.url)
        request.user = self.user
        resp = self.view(request)
        data = json.loads(resp.content.decode('UTF-8'))
        self.assertEqual(self.expected, data)

    # searching by James Bond should only yield James Bond
    def test_incomplete_matching(self):
        james_patient, sam_episode = self.create_patient(
            "James", "Bond", "23412"
        )
        sam_patient, sam_episode = self.create_patient(
            "Samantha", "Bond", "23432"
        )
        blofeld_patient, blofeld_episode = self.create_patient(
            "Ernst", "Blofeld", "23422"
        )
        resp = self.get_response('{}/?query=James%20Bond'.format(self.url))
        data = json.loads(resp.content.decode('UTF-8'))["object_list"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["first_name"], "James")
        self.assertEqual(data[0]["surname"], "Bond")

    def test_number_of_queries(self):
        """ Pagination should make sure we
            do the same number of queries
            despite the number of results.
        """
        # we need to make sure we're all logged in before we start
        self.assertIsNotNone(self.user)
        for i in range(100):
            self.create_patient(
                "James", "Bond", str(i)
            )

        with self.assertNumQueries(36):
            self.get_response('{}/?query=Bond'.format(self.url))

        for i in range(20):
            self.create_patient(
                "James", "Blofelt", str(i)
            )

        with self.assertNumQueries(36):
            self.get_response('{}/?query=Blofelt'.format(self.url))

    def test_with_multiple_patient_episodes(self):
        self.patient.create_episode()
        blofeld_patient, blofeld_episode = self.create_patient(
            "Ernst", "Blofeld", "23422"
        )
        response = json.loads(
            self.get_response(
                '{}/?query=Blofeld'.format(self.url)
            ).content.decode('UTF-8')
        )
        expected = {
            "total_pages": 1,
            "object_list": [{
                "count": 1,
                "first_name": "Ernst",
                "surname": "Blofeld",
                "start": None,
                "patient_id": 2,
                "hospital_number": "23422",
                "date_of_birth": None,
                "end": None,
                "id": 2,
                "categories": ["Inpatient"]
            }],
            "page_number": 1,
            "total_count": 1
        }
        self.assertEqual(response, expected)


class SearchTemplateTestCase(OpalTestCase):

    def test_search_template_view(self):
        self.assertStatusCode('/search/templates/search.html/', 200)


class ExtractSearchViewTestCase(BaseSearchTestCase):

    def test_not_logged_in_post(self):
        view = views.ExtractSearchView()
        view.request = self.get_not_logged_in_request()
        with self.assertRaises(PermissionDenied):
            view.post()

    def test_post(self):
        data = json.dumps([
            {
                u'page_number': 1,
                u'rule': u'demographics',
                u'field': u'surname',
                u'combine': u'and',
                u'value': u'Connery',
                u'query_type': u'Equals'
            }
        ])
        request = self.rf.post('extract')
        request.user = self.user
        view = views.ExtractSearchView()
        view.request = request
        with patch.object(view.request, 'read') as mock_read:
            mock_read.return_value = data

            resp = json.loads(view.post().content.decode('UTF-8'))
            self.assertEqual(1, resp['total_count'])
            self.assertEqual(self.patient.id, resp['object_list'][0]['patient_id'])

    def test_post_with_no_data(self):
        data = json.dumps([])
        request = self.rf.post('extract')
        request.user = self.user
        view = views.ExtractSearchView()
        view.request = request
        with patch.object(view.request, 'read') as mock_read:
            mock_read.return_value = data
            resp = view.post()
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(json.loads(resp.content.decode('UTF-8')), dict(
                error="No search criteria provied"
            ))


class ExtractStatusViewTestCase(BaseSearchTestCase):

    @patch('celery.result.AsyncResult')
    def test_get(self, async_result):
        view = views.ExtractStatusView()
        view.request = self.get_logged_in_request()
        async_result.return_value.state = 'The State'
        resp = view.get(task_id=490)
        self.assertEqual(200, resp.status_code)


class ExtractFileView(BaseSearchTestCase):

    def test_get_not_logged_in(self):
        view = views.ExtractFileView()
        view.request = self.get_not_logged_in_request()
        with self.assertRaises(PermissionDenied):
            resp = view.get(task_id=8902321890)

    @patch('celery.result.AsyncResult')
    def test_get(self, async_result):
        view = views.ExtractFileView()
        view.request = self.get_logged_in_request()
        async_result.return_value.state = 'SUCCESS'
        async_result.return_value.get.return_value = 'foo.txt'

        m = mock_open(read_data='This is a file')
        with patch('search.views.open', m, create=True) as m:
            resp = view.get(task_id=437878)
            self.assertEqual(200, resp.status_code)

    @patch('celery.result.AsyncResult')
    def test_get_not_successful(self, async_result):
        view = views.ExtractFileView()
        view.request = self.get_logged_in_request("/")
        async_result.return_value.state = 'FAILURE'
        with self.assertRaises(ValueError):
            view.get(task_id=8902321890)


class DownloadTestCase(BaseSearchTestCase):
    def setUp(self):
        super(DownloadTestCase, self).setUp()
        self.url = reverse('extract_download')

    @override_settings(
        EXTRACT_ASYNC=True
    )
    @patch('search.views.async_extract')
    def test_async_integrations(self, async_extract):
        async_extract.return_value = 1
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )
        query = dict(
            criteria=[{
                "combine": "and",
                "rule": "demographics",
                "field": "hospital_number",
                "query_type": "Contains",
                "value": "a",
            }],
            data_slice={}
        )
        post_data = json.dumps({
            "criteria":
                json.dumps(query["criteria"]),
            "data_slice": json.dumps(query["data_slice"])
        })
        create_task = self.client.post(
            self.url, post_data, content_type='appliaction/json'
        )
        self.assertEqual(create_task.status_code, 200)
        content = json.loads(create_task.content.decode())
        status_url = reverse('extract_status', kwargs=dict(
            task_id=content["extract_id"]
        ))

        status_result = self.client.get(status_url)
        self.assertEqual(status_result.status_code, 200)
        self.assertEqual(
            json.loads(status_result.content.decode())['state'],
            "PENDING"
        )
        self.assertEqual(async_extract.call_count, 1)
        async_extract.assert_called_once_with(self.user, query)

    @override_settings(EXTRACT_ASYNC=False)
    def test_non_async_extract(self):
        # a vanilla check to make sure that the view returns a zip file
        url = reverse("extract_download")
        post_data = {
            "criteria":
                json.dumps([{
                    "combine": "and",
                    "rule": "demographics",
                    "field": "hospital_number",
                    "query_type": "Contains",
                    "value": "a",
                }]),
        }

        self.assertTrue(
            self.client.login(
                username=self.user.username,
                password=self.PASSWORD
            )
        )

        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)

    def test_non_asyc_extract_with_slice(self):
        url = reverse("extract_download")
        post_data = {
            "criteria":
                json.dumps([{
                    "combine": "and",
                    "rule": "demographics",
                    "field": "hospital_number",
                    "query_type": "Contains",
                    "value": "a",
                }]),
            "data_slice":
                json.dumps({
                    "demographics": ["date_of_birth"]
                })
        }

        self.assertTrue(
            self.client.login(
                username=self.user.username,
                password=self.PASSWORD
            )
        )

        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)

    def test_generate_zip(self):
        m = mock_open(read_data='This is a file')
        url = reverse("extract_download")
        criteria = [{
            "combine": "and",
            "rule": "demographics",
            "field": "hospital_number",
            "query_type": "Contains",
            "value": "007",
        }]

        data_slice = {
            "demographics": ["date_of_birth"]
        }
        post_data = {
            "criteria":
                json.dumps(criteria),
            "data_slice":
                json.dumps(data_slice)
        }

        self.assertTrue(
            self.client.login(
                username=self.user.username,
                password=self.PASSWORD
            )
        )

        with patch('search.views.open', m, create=True):
            with patch(
                'search.views.queries.create_query',
                side_effect=queries.create_query
            ) as create_query:
                with patch(
                    'search.views.zip_archive',
                    side_effect=extract.zip_archive
                ) as zip_archive:
                    m().read.return_value = "something"
                    response = self.client.post(url, post_data)

        self.assertEqual(
            create_query.call_args[0][0].username, 'testuser'
        )
        self.assertEqual(
            create_query.call_args[0][1], criteria
        )

        # asserting the response of the query
        self.assertEqual(
            zip_archive.call_args[0][0][0], self.episode
        )

        # asserting that some form of description is returned
        self.assertTrue(
            isinstance(zip_archive.call_args[0][1], str)
        )

        # assert that the user is passed in
        self.assertEqual(
            zip_archive.call_args[0][2].username, 'testuser'
        )

        # assert that the data slice is passed in
        self.assertEqual(
            zip_archive.call_args[1]["fields"], data_slice
        )

        self.assertTrue(m.call_args[0][0].endswith('extract.zip'))
        self.assertEqual(response.status_code, 200)
