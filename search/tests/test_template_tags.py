from opal.core.test import OpalTestCase
from search.templatetags import search_string_utils


class SearchStringUtilsTemplateTagsTestCase(OpalTestCase):
    def test_underscore_to_spaces(self):
        self.assertEqual(
            search_string_utils.underscore_to_spaces("some_thing"),
            "some thing"
        )

    def test_underscore_to_spaces_no_spaces(self):
        self.assertEqual(
            search_string_utils.underscore_to_spaces("something"),
            "something"
        )
