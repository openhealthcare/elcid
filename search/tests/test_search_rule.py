from mock import MagicMock, patch
import datetime

from opal.core.test import OpalTestCase
from search import search_rules
from search import search_rule_fields
from search import exceptions


class SearchRuleFieldTestCase(OpalTestCase):
    def setUp(self, *args, **kwargs):
        class SomeSearchRuleField(search_rule_fields.SearchRuleField):
            lookup_list = "some_list"
            enum = [1, 2, 3]
            description = "its a custom field"
            display_name = "custom field you know"
            field_type = "string"
            field_name = "some_slug"
            type_display_name = "some field"
            widget = "some_widget.html"
        self.custom_field = SomeSearchRuleField(self.user)
        super(SearchRuleFieldTestCase, self).setUp(*args, **kwargs)

    def test_slug_if_slug_provided(self):
        self.assertEqual(self.custom_field.get_name(), "some_slug")

    def test_query(self):
        with self.assertRaises(NotImplementedError) as nie:
            self.custom_field.query("some query")

        self.assertEqual("please implement a query", str(nie.exception))

    def test_to_dict(self):
        expected = dict(
            lookup_list="some_list",
            enum=[1, 2, 3],
            query_args=['value', 'query_type'],
            name="some_slug",
            widget='some_widget.html',
            widget_description='partials/search/descriptions/widget_description.html',
            display_name='custom field you know',
        )
        self.assertEqual(
            self.custom_field.to_dict(),
            expected
        )


class SearchRuleTestCase(OpalTestCase):
    def test_query(self):
        some_mock_query = MagicMock()

        with patch.object(
            search_rules.SearchRule, "get_field"
        ) as get_field:
            get_field.return_value = some_mock_query
            some_mock_query.query.return_value = "some_result"
            query = dict(field="tree")
            result = search_rules.SearchRule(self.user).query(query)
            self.assertEqual(result, "some_result")
            some_mock_query.query.assert_called_once_with(query)


class EpisodeQueryTestCase(OpalTestCase):
    def setUp(self, *args, **kwargs):
        super(EpisodeQueryTestCase, self).setUp(*args, **kwargs)
        _, self.episode = self.new_patient_and_episode_please()
        self.episode.start = datetime.date(2017, 1, 1)
        self.episode.end = datetime.date(2017, 1, 5)
        self.episode.save()
        self.episode_rule = search_rules.EpisodeRule(self.user)

    def test_episode_end_start(self):
        query_end = dict(
            query_type="Before",
            value="1/8/2017",
            field="end"
        )
        self.assertEqual(
            list(self.episode_rule.query(query_end))[0], self.episode
        )

    def test_episode_end_when_none(self):
        self.episode.end = None
        self.episode.save()
        query_end = dict(
            query_type="Before",
            value="1/8/2017",
            field="end"
        )
        self.assertEqual(
            list(self.episode_rule.query(query_end)), []
        )

    def test_episode_end_after(self):
        query_end = dict(
            query_type="After",
            value="1/8/2015",
            field="end"
        )
        self.assertEqual(
            list(self.episode_rule.query(query_end))[0], self.episode
        )

    def test_episode_end_not_found(self):
        query_end = dict(
            query_type="Before",
            value="1/8/2010",
            field="end"
        )
        self.assertEqual(
            list(self.episode_rule.query(query_end)), []
        )

    def test_episode_end_wrong_query_param(self):
        query_end = dict(
            query_type="asdfsadf",
            value="1/8/2010",
            field="end"
        )
        with self.assertRaises(exceptions.SearchException):
            self.episode_rule.query(query_end)

    def test_episode_start_before(self):
        query_end = dict(
            query_type="Before",
            value="1/8/2017",
            field="start"
        )
        self.assertEqual(
            list(self.episode_rule.query(query_end))[0], self.episode
        )

    def test_episode_start_after(self):
        query_end = dict(
            query_type="After",
            value="1/8/2015",
            field="start"
        )
        self.assertEqual(
            list(self.episode_rule.query(query_end))[0], self.episode
        )

    def test_episode_start_when_none(self):
        self.episode.start = None
        self.episode.save()
        query_end = dict(
            query_type="Before",
            value="1/8/2017",
            field="start"
        )
        self.assertEqual(
            list(self.episode_rule.query(query_end)), []
        )

    def test_episode_start_not_found(self):
        query_end = dict(
            query_type="Before",
            value="1/8/2011",
            field="start"
        )
        self.assertEqual(
            list(self.episode_rule.query(query_end)), []
        )

    def test_episode_start_wrong_query_param(self):
        query_end = dict(
            query_type="asdfsadf",
            value="1/8/2010",
            field="start"
        )
        with self.assertRaises(exceptions.SearchException):
            self.episode_rule.query(query_end)


class EpisodeTeamQueryTestCase(OpalTestCase):
    def setUp(self, *args, **kwargs):
        super(EpisodeTeamQueryTestCase, self).setUp(*args, **kwargs)
        _, self.episode_1 = self.new_patient_and_episode_please()
        _, self.episode_2 = self.new_patient_and_episode_please()
        _, self.episode_3 = self.new_patient_and_episode_please()
        self.episode_rule = search_rules.EpisodeRule(self.user)

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

    def test_episode_team_unknown_team(self):
        query_end = dict(
            query_type="Any Of",
            value=["Some Team"],
            field="team"
        )
        with self.assertRaises(exceptions.SearchException) as er:
            self.episode_rule.query(query_end)
        self.assertEqual(
            str(er.exception),
            "unable to find the tag titled Some Team"
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


class LocationRuleTestCase(OpalTestCase):
    def test_location_rule_order(self):
        location_rule = search_rules.SearchRule.get_rule(
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
        episode_rule = search_rules.SearchRule.get_rule(
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
