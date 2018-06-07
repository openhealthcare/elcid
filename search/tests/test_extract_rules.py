import mock
from opal.core.test import OpalTestCase
from opal.tests import models
from search import extract_rules

# HoundOwner is an episode subrecord, HouseOwner is a patient subrecord
# HatWearer is an episode subrecord with many to many
from opal.tests.models import HoundOwner, HouseOwner, HatWearer, Hat


class CsvFieldWrapperTestCase(OpalTestCase):
    def get_field(self, model, field_name):
        rule = extract_rules.ExtractRule.get_rule(model.get_api_name(), self.user)
        return rule.get_field(field_name)

    def test_csv_field_wrapper_get_description_template_boolean(self):
        expected = "search/field_descriptions/boolean.html"
        rule = self.get_field(models.HatWearer, "wearing_a_hat")
        self.assertEqual(
            rule.get_description_template(),
            expected
        )

    def test_csv_field_wrapper_get_description_template_date_time(self):
        expected = "search/field_descriptions/date_time.html"
        rule = self.get_field(models.Birthday, "party")
        self.assertEqual(
            rule.get_description_template(),
            expected
        )

    def test_csv_field_wrapper_get_description_template_date(self):
        expected = "search/field_descriptions/date.html"
        rule = self.get_field(models.Birthday, "birth_date")
        self.assertEqual(
            rule.get_description_template(),
            expected
        )

    def test_csv_field_wrapper_get_description_template_text(self):
        expected = "search/field_descriptions/text.html"
        rule = self.get_field(models.Dinner, "food")
        self.assertEqual(
            rule.get_description_template(),
            expected
        )

    def test_csv_field_wrapper_get_description_template_fk_or_ft(self):
        expected = "search/field_descriptions/text.html"
        rule = self.get_field(models.HoundOwner, "dog")
        self.assertEqual(
            rule.get_description_template(),
            expected
        )

    def test_csv_field_wrapper_get_description_template_numeric(self):
        expected = "search/field_descriptions/number.html"
        rule = self.get_field(models.FavouriteNumber, "number")
        self.assertEqual(
            rule.get_description_template(),
            expected
        )

    def test_csv_field_wrapper_get_description_template_other(self):
        # testing with a time field as currently this does not
        # have a display template
        expected = "search/field_descriptions/generic.html"
        rule = self.get_field(models.Dinner, "time")
        self.assertEqual(
            rule.get_description_template(),
            expected
        )


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
    def setUp(self):
        self.rule = extract_rules.ExtractRule.get_rule(
            "episode", self.user
        )

    def test_field_order(self):
        fields = self.rule.get_fields()
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
            fields[3].get_name(), "category_name"
        )
        self.assertEqual(
            fields[4].get_name(), "start"
        )
        self.assertEqual(
            fields[5].get_name(), "end"
        )

    def test_get_fields_for_schema(self):
        fields = self.rule.get_fields_for_schema()
        field_names = {i.get_name() for i in fields}
        self.assertNotIn("patient_id", field_names)
        self.assertNotIn("id", field_names)

    @mock.patch(
        "search.extract_rules.subrecord_discoverable\
.get_team_display_name_to_slug"
    )
    def test_team_extract_with_multiple_tags(
        self, get_team_display_name_to_slug
    ):
        get_team_display_name_to_slug.return_value = {
            "This": "this",
            "That": "that"
        }
        _, episode = self.new_patient_and_episode_please()
        episode.set_tag_names(["this", "that"], self.user)
        team_rule = self.rule.get_field("team")
        result = team_rule.extract(episode)
        self.assertEqual("This; That", result)

    @mock.patch("search.extract_rules.episodes.EpisodeCategory.list")
    def test_episode_category_enum(self, categories):

        class InpatientCategory(object):
            display_name = "Inpatient"

        categories.return_value = [InpatientCategory]
        self.assertEqual(
            ["Inpatient"], self.rule.get_field("category_name").enum
        )


class ManyToManyTestCase(OpalTestCase):
    def setUp(self, *args, **kwargs):
        super(ManyToManyTestCase, self).setUp(*args, **kwargs)
        _, self.episode = self.new_patient_and_episode_please()
        self.bowler = Hat.objects.create(name="bowler")
        self.top = Hat.objects.create(name="top")
        self.hat_wearer_rule = extract_rules.ExtractRule.get_rule(
            HatWearer.get_api_name(), self.user
        )
        self.hat_field = self.hat_wearer_rule.get_field("hats")
        self.hat_wearer = HatWearer.objects.create(
            episode=self.episode
        )

    def test_extract_single_many_to_many_field(self):
        self.hat_wearer.hats.add(self.bowler)
        self.assertEqual(
            self.hat_field.extract(self.hat_wearer),
            "bowler"
        )

    def test_extract_multi_many_to_many_field(self):
        self.hat_wearer.hats.add(self.bowler, self.top)
        self.assertEqual(
            self.hat_field.extract(self.hat_wearer),
            "bowler; top"
        )

    def test_extract_empty_many_to_many_field(self):
        self.assertEqual(self.hat_field.extract(self.hat_wearer), "")
