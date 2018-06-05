from opal.core.test import OpalTestCase
from search import extract_rules


class DemographicsExtractRuleTestCase(OpalTestCase):
    def test_required_fields(self):
        demographics = extract_rules.ExtractRule.get_rule("demographics", self.user)
        self.assertTrue(demographics.get_field("sex").required)
        self.assertTrue(demographics.get_field("date_of_birth").required)


class LocationRuleTestCase(OpalTestCase):
    def test_location_rule_order(self):
        location_rule = extract_rules.ExtractRule.get_rule(
            "location", self.user
        )
        fields = location_rule.get_fields()
        self.assertEqual(
            fields[0].get_name(), "bed"
        )
        self.assertEqual(
            fields[1].get_name(), "ward"
        )
        self.assertEqual(
            fields[2].get_name(), "hospital"
        )


class EpisodeTestBase(OpalTestCase):
    def test_field_order(self):
        episode_rule = extract_rules.ExtractRule.get_rule(
            "episode", self.user
        )
        fields = episode_rule.get_fields()
        self.assertEqual(
            fields[0].get_name(), "team"
        )
        self.assertEqual(
            fields[1].get_name(), "start"
        )
        self.assertEqual(
            fields[2].get_name(), "end"
        )
