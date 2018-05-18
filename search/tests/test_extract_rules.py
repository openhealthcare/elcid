from opal.core.test import OpalTestCase
from search.extract_rules import ExtractRule


class DemographicsExtractRuleTestCase(OpalTestCase):
    def test_required_fields(self):
        demographics = ExtractRule.get("demographics", self.user)
        self.assertTrue(demographics.get_field("sex").required)
        self.assertTrue(demographics.get_field("date_of_birth").required)

    def test_to_dict(self):
        pass
