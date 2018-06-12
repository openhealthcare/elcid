from mock import patch

from opal.core.test import OpalTestCase
from search import exceptions
from search import search_rules
from search import search_rule_fields


class EpisodeTeamQueryTestCase(OpalTestCase):
    def setUp(self, *args, **kwargs):
        super(EpisodeTeamQueryTestCase, self).setUp(*args, **kwargs)
        _, self.episode_1 = self.new_patient_and_episode_please()
        _, self.episode_2 = self.new_patient_and_episode_please()
        _, self.episode_3 = self.new_patient_and_episode_please()
        self.episode_rule = search_rules.EpisodeSearchRule(self.user)

    def test_episode_team_wrong_query_param(self):
        query_end = dict(
            query_type="asdfsadf",
            value=["Some Team"],
            field="team"
        )
        with self.assertRaises(exceptions.SearchException) as er:
            self.episode_rule.query(query_end)
        self.assertEqual(
            str(er.exception),
            "unrecognised query type for the episode team query with asdfsadf"
        )

    def test_episode_team_all_of_one(self):
        """
            test all of with a single tag
        """
        self.episode_1.tagging_set.create(value="tree", archived=False)
        self.episode_1.tagging_set.create(value="plant", archived=False)
        self.episode_2.tagging_set.create(value="plant", archived=False)
        self.episode_3.tagging_set.create(value="tree", archived=False)
        query_end = dict(
            query_type="All Of",
            value=["Plant"],
            field="team"
        )
        with patch.object(search_rule_fields.models.Tagging, "build_field_schema") as bfs:
            bfs.return_value = [
                dict(
                    name="plant",
                    title="Plant"
                ),
                dict(
                    name="tree",
                    title="Tree"
                ),
            ]
            result = self.episode_rule.query(query_end)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, self.episode_1.id)
        self.assertEqual(result[1].id, self.episode_2.id)

    def test_episode_team_all_of_archived(self):
        """
            test archived tags are returned
        """
        self.episode_1.tagging_set.create(value="plant", archived=True)
        query_end = dict(
            query_type="All Of",
            value=["Plant"],
            field="team"
        )
        with patch.object(search_rule_fields.models.Tagging, "build_field_schema") as bfs:
            bfs.return_value = [
                dict(
                    name="plant",
                    title="Plant"
                ),
                dict(
                    name="tree",
                    title="Tree"
                ),
            ]
            result = self.episode_rule.query(query_end)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.episode_1.id)

    def test_episode_team_all_of_many(self):
        """
            test when looking for multiple tags only
            episodes with all of those tags will be returned
        """
        self.episode_1.tagging_set.create(value="tree", archived=False)
        self.episode_1.tagging_set.create(value="plant", archived=False)
        self.episode_2.tagging_set.create(value="plant", archived=False)
        self.episode_3.tagging_set.create(value="tree", archived=False)
        query_end = dict(
            query_type="All Of",
            value=["Plant", "Tree"],
            field="team"
        )
        with patch.object(
            search_rule_fields.models.Tagging, "build_field_schema"
        ) as bfs:
            bfs.return_value = [
                dict(
                    name="plant",
                    title="Plant"
                ),
                dict(
                    name="tree",
                    title="Tree"
                ),
            ]
            result = self.episode_rule.query(query_end)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.episode_1.id)

    @patch("search.search_rule_fields.models.Tagging.build_field_schema")
    def test_episode_team_enum(self, bfs):
        bfs.return_value = [
            dict(
                name="plant",
                title="Plant"
            ),
            dict(
                name="tree",
                title="Tree"
            ),
        ]
        self.assertEqual(
            ["Plant", "Tree"], self.episode_rule.get_field("team").enum
        )

    def test_episide_team_any_of_one(self):
        """
            test all of with a single tag
        """
        self.episode_1.tagging_set.create(value="tree", archived=False)
        self.episode_1.tagging_set.create(value="plant", archived=False)
        self.episode_2.tagging_set.create(value="plant", archived=False)
        self.episode_3.tagging_set.create(value="tree", archived=False)
        query_end = dict(
            query_type="Any Of",
            value=["Plant"],
            field="team"
        )
        with patch.object(
            search_rule_fields.models.Tagging, "build_field_schema"
        ) as bfs:
            bfs.return_value = [
                dict(
                    name="plant",
                    title="Plant"
                ),
                dict(
                    name="tree",
                    title="Tree"
                ),
            ]
            result = self.episode_rule.query(query_end)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, self.episode_1.id)
        self.assertEqual(result[1].id, self.episode_2.id)

    def test_episide_team_any_of_many(self):
        """
            test when looking for multiple tags only
            episodes with all of those tags will be returned
        """
        self.episode_1.tagging_set.create(value="tree", archived=False)
        self.episode_1.tagging_set.create(value="plant", archived=False)
        self.episode_2.tagging_set.create(value="plant", archived=False)
        self.episode_3.tagging_set.create(value="tree", archived=False)
        query_end = dict(
            query_type="Any Of",
            value=["Plant", "Tree"],
            field="team"
        )

        with patch.object(
            search_rule_fields.models.Tagging, "build_field_schema"
        ) as bfs:
            bfs.return_value = [
                dict(
                    name="plant",
                    title="Plant"
                ),
                dict(
                    name="tree",
                    title="Tree"
                ),
            ]
            result = self.episode_rule.query(query_end)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].id, self.episode_1.id)
        self.assertEqual(result[1].id, self.episode_2.id)
        self.assertEqual(result[2].id, self.episode_3.id)


class EpisoseCategoryTestCase(OpalTestCase):
    def setUp(self, *args, **kwargs):
        super(EpisoseCategoryTestCase, self).setUp(*args, **kwargs)
        _, self.episode_1 = self.new_patient_and_episode_please()
        self.episode_1.category_name = "Inpatient"
        self.episode_1.save()

        _, self.episode_2 = self.new_patient_and_episode_please()
        self.episode_2.category_name = "Out patient"
        self.episode_2.save()

        _, self.episode_3 = self.new_patient_and_episode_please()
        self.episode_3.category_name = "Inpatient"
        self.episode_3.save()

        _, self.episode_4 = self.new_patient_and_episode_please()
        self.episode_4.category_name = "Other"
        self.episode_4.save()

        self.rule_field = search_rule_fields.EpisodeCategory(self.user)

    @patch("search.search_rule_fields.episodes.EpisodeCategory.list")
    def test_episode_category_enum(self, categories):

        class InpatientCategory(object):
            display_name = "Inpatient"

        categories.return_value = [InpatientCategory]
        self.assertEqual(
            ["Inpatient"], self.rule_field.enum
        )

    def test_episode_category_contains(self):
        given_query = dict(
            query_type="Contains",
            value="patient",
        )
        result = self.rule_field.query(given_query)
        self.assertEqual(
            set(result),
            {self.episode_1, self.episode_2, self.episode_3}
        )

    def test_episode_category_contains_none(self):
        given_query = dict(
            query_type="Contains",
            value="non existent",
        )
        result = self.rule_field.query(given_query)
        self.assertFalse(result.exists())

    def test_episode_category_exact(self):
        given_query = dict(
            query_type="Equals",
            value="Inpatient",
        )
        result = self.rule_field.query(given_query)
        self.assertEqual(
            set(result),
            {self.episode_1, self.episode_3}
        )

    def test_episode_category_exact_none(self):
        given_query = dict(
            query_type="Equals",
            value="non existent",
        )
        result = self.rule_field.query(given_query)
        self.assertFalse(result.exists())

    def test_category_unknown_query(self):
        given_query = dict(
            query_type="blah blah",
            value="non existent",
        )
        e = "unrecognised query type for the episode category query with blah \
blah"
        with self.assertRaises(exceptions.SearchException) as se:
            self.rule_field.query(given_query)
        self.assertEqual(str(se.exception), e)
