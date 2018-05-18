"""
Unittests for the search.tasks module
"""
from mock import patch
from opal.core.test import OpalTestCase

from search import tasks


class ExtractTestCase(OpalTestCase):

    @patch('search.extract.zip_archive')
    def test_extract(self, zip_archive):
        zip_archive.return_value = 'Help'
        data_slice = {}
        criteria = [
            {
                u'rule': u'demographics',
                u'field': u'surname',
                u'combine': u'and',
                u'value': u'Stevens',
                u'query_type': u'Equals'
            }
        ]
        extract_query = dict(
            data_slice=data_slice,
            criteria=criteria
        )
        fname = tasks.extract(self.user, extract_query)
        self.assertEqual('Help', fname)
