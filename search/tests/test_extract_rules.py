from opal.core.test import OpalTestCase
from search import extract_rules

# HoundOwner is an episode subrecord, HouseOwner is a patient subrecord
from opal.tests.models import HoundOwner, HouseOwner


class ExtractRuleTestCase(OpalTestCase):
    def test_get_episode_subrecord_fields(self):
        """
        episode subrecords should add the patient id
        """
        rule = extract_rules.ExtractRule.get_rule(
            HoundOwner.get_api_name(), self.user
        )
        field_names = [i.get_name() for i in rule.get_fields()]
        self.assertIn("patient_id", field_names)
        self.assertIn("episode_id", field_names)

    def test_get_patient_subrecord_fields(self):
        """
        patient subrecords should contain the patient id
        """
        rule = extract_rules.ExtractRule.get_rule(
            HouseOwner.get_api_name(), self.user
        )
        field_names = [i.get_name() for i in rule.get_fields()]
        self.assertIn("patient_id", field_names)

    def test_extract_patient_id_for_episode_subrecord(self):
        rule = extract_rules.ExtractRule.get_rule(
            HoundOwner.get_api_name(), self.user
        )
        field = rule.get_field("patient_id")
        patient, _ = self.new_patient_and_episode_please()
        # do this so we can be sure that the episode id is different
        # from the patient id
        episode = patient.create_episode()
        self.assertEqual(patient.id, 1)
        self.assertEqual(episode.id, 2)
        hound_owner = HoundOwner.objects.create(episode=episode)
        self.assertEqual(field.extract(hound_owner), 1)


class DemographicsExtractRuleTestCase(OpalTestCase):
    def test_required_fields(self):
        demographics = extract_rules.ExtractRule.get_rule(
            "demographics", self.user
        )
        self.assertTrue(demographics.get_field("sex").required)
        self.assertTrue(demographics.get_field("date_of_birth").required)


class LocationRuleTestCase(OpalTestCase):
    def test_location_rule_order(self):
        location_rule = extract_rules.ExtractRule.get_rule(
            "location", self.user
        )
        fields = location_rule.get_fields()
        self.assertEqual(
            fields[0].get_name(), "patient_id"
        )

        self.assertEqual(
            fields[1].get_name(), "episode_id"
        )

        self.assertEqual(
            fields[2].get_name(), "bed"
        )
        self.assertEqual(
            fields[3].get_name(), "ward"
        )
        self.assertEqual(
            fields[4].get_name(), "hospital"
        )


class EpisodeTestBase(OpalTestCase):
    def test_field_order(self):
        episode_rule = extract_rules.ExtractRule.get_rule(
            "episode", self.user
        )
        fields = episode_rule.get_fields()
        self.assertEqual(
            fields[0].get_name(), "patient_id"
        )
        self.assertEqual(
            fields[1].get_name(), "id"
        )
        self.assertEqual(
            fields[2].get_name(), "team"
        )
        self.assertEqual(
            fields[3].get_name(), "start"
        )
        self.assertEqual(
            fields[4].get_name(), "end"
        )

    def test_get_fields_for_schema(self):
        episode_rule = extract_rules.ExtractRule.get_rule(
            "episode", self.user
        )
        fields = episode_rule.get_fields_for_schema()
        field_names = {i.get_name() for i in fields}
        self.assertNotIn("patient_id", field_names)
        self.assertNotIn("id", field_names)
