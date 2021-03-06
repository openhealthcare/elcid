"""
Unittests for search.queries
"""
from datetime import date, datetime

from django.contrib.contenttypes.models import ContentType
from mock import patch, MagicMock
from opal.tests.episodes import RestrictedEpisodeCategory

from search.search_rules import SearchRule
from opal.models import Synonym, Gender, Patient, Episode

from opal.core.test import OpalTestCase

from search import queries

from opal.tests import models as testmodels
from elcid import models


# don't remove this, we use it to discover the restricted episode category
from opal.tests.episodes import RestrictedEpisodeCategory  # NOQA


class QueryBackendTestCase(OpalTestCase):

    def test_fuzzy_query(self):
        with self.assertRaises(NotImplementedError):
            queries.QueryBackend(self.user, 'aquery').fuzzy_query()

    def test_get_episodes(self):
        with self.assertRaises(NotImplementedError):
            queries.QueryBackend(self.user, 'aquery').get_episodes()

    def test_description(self):
        with self.assertRaises(NotImplementedError):
            queries.QueryBackend(self.user, 'aquery').description()

    def test_get_patients(self):
        with self.assertRaises(NotImplementedError):
            queries.QueryBackend(self.user, 'aquery').get_patients()

    def test_get_patient_summaries(self):
        with self.assertRaises(NotImplementedError):
            queries.QueryBackend(self.user, 'aquery').get_patient_summaries(
                Patient.objects.all()
            )

    def test_sort_patients(self):
        with self.assertRaises(NotImplementedError):
            queries.QueryBackend(self.user, 'aquery').sort_patients(
                Patient.objects.all()
            )


class DatabaseQueryTestCase(OpalTestCase):
    DATE_OF_BIRTH = date(day=27, month=1, year=1977)
    DATE_OF_EPISODE = date(day=1, month=2, year=2015)

    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.episode.date_of_episode = self.DATE_OF_EPISODE
        self.episode.start = self.DATE_OF_EPISODE
        self.episode.end = self.DATE_OF_EPISODE
        self.episode.save()
        self.demographics = self.patient.demographics_set.get()
        self.demographics.first_name = "Sally"
        self.demographics.surname = "Stevens"
        self.demographics.sex = "Female"
        self.demographics.hospital_number = "0"
        self.demographics.date_of_birth = self.DATE_OF_BIRTH
        self.demographics.save()

        self.name_criteria = [
            {
                u'rule': u'demographics',
                u'field': u'surname',
                u'combine': u'and',
                u'value': u'Stevens',
                u'query_type': u'Equals'
            }
        ]

    def test_episodes_for_boolean_fields(self):
        criteria = dict(
            rule='demographics', field='death_indicator',
            combine='and', value='false'
        )
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_number_fields_greater_than(self):
        testmodels.FavouriteNumber.objects.create(
            patient=self.patient, number=10
        )
        criteria = dict(
            rule='favourite_number',
            field='number',
            combine='and',
            value=1,
            query_type='Greater Than'
        )
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

        criteria["query"] = 100
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_sort_patients(self):
        patient_1, episode_1 = self.new_patient_and_episode_please()
        patient_2, episode_2 = self.new_patient_and_episode_please()
        patient_1.create_episode()

        not_used_patient, _ = self.new_patient_and_episode_please()
        query = queries.DatabaseQuery(self.user, [self.name_criteria])
        result = query.sort_patients(
            Patient.objects.exclude(id=not_used_patient.id)
        )

        # should start with patient 1, because its got 2 episodes
        self.assertEqual(
            result[0].id, patient_1.id,
        )

        self.assertEqual(
            result[1].id, patient_2.id,
        )

        # make sure its true even if we reverse it
        result = query.sort_patients(
            Patient.objects.exclude(id=not_used_patient.id).order_by("-id")
        )
        self.assertEqual(
            result[0].id, patient_1.id,
        )

        self.assertEqual(
            result[1].id, patient_2.id,
        )

    def test_episodes_for_number_fields_less_than(self):
        testmodels.FavouriteNumber.objects.create(
            patient=self.patient, number=10
        )
        criteria = dict(
            rule='favourite_number',
            field='number',
            combine='and',
            value=11,
            query_type='Less Than'
        )
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

        criteria["query"] = 1
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_boolean_fields_episode_subrecord(self):
        criteria = dict(
            rule='hat_wearer', field='wearing_a_hat',
            combine='and', value='true'
        )
        hatwearer = testmodels.HatWearer(
            episode=self.episode, wearing_a_hat=True
        )
        hatwearer.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_date_fields(self):
        criteria = dict(
            rule='dog_owner', field='ownership_start_date',
            combine='and', value='2/12/1999', query_type='Before'
        )
        dogowner = testmodels.DogOwner(
            episode=self.episode, ownership_start_date=date(1999, 12, 1))
        dogowner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_date_fields_patient_subrecord(self):
        criteria = dict(
            rule='birthday', field='birth_date',
            combine='and', value='2/12/1999', query_type='Before'
        )
        birthday = testmodels.Birthday(
            patient=self.patient, birth_date=date(1999, 12, 1))
        birthday.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_date_fields_before(self):
        criteria = dict(
            rule='dog_owner', field='ownership_start_date',
            combine='and', value='1/12/2000', query_type='Before'
        )
        dogowner = testmodels.DogOwner(
            episode=self.episode, ownership_start_date=date(1999, 12, 1))
        dogowner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_date_fields_after(self):
        criteria = dict(
            rule='dog_owner', field='ownership_start_date',
            combine='and', value='1/12/1998', query_type='After'
        )
        dogowner = testmodels.DogOwner(
            episode=self.episode, ownership_start_date=date(1999, 12, 1))
        dogowner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    @patch("search.queries.datetime")
    def test_description_display_name(self, dt):
        dt.datetime.now.return_value = datetime(
            2017, 12, 1, 10, 10
        )
        criteria = dict(
            rule='hat_wearer', field='name',
            combine='and', value='jeff', query_type='Contains'
        )
        query = queries.DatabaseQuery(self.user, [criteria])
        exp = "testuser (01/12/2017 10:10:00)\nSearching for:\nWearer of Hats \
Name contains jeff"
        self.assertEqual(exp, query.description())

    @patch("search.queries.datetime")
    def test_description_field_display_name(self, dt):
        dt.datetime.now.return_value = datetime(
            2017, 12, 1, 10, 10
        )

        criteria = dict(
            rule='hound_owner', field='dog',
            combine='and', value='jeff', query_type='Contains'
        )
        query = queries.DatabaseQuery(self.user, [criteria])
        exp = """
testuser (01/12/2017 10:10:00)
Searching for:
Hound Owner Hound contains jeff
""".strip()
        self.assertEqual(exp, query.description())

    @patch("search.queries.datetime")
    def test_description_multiple(self, dt):
        dt.datetime.now.return_value = datetime(
            2017, 12, 1, 10, 10
        )

        criteria_1 = dict(
            rule='hat_wearer', field='name',
            combine='and', value='jeff', query_type='Contains'
        )

        criteria_2 = dict(
            rule='hound_owner', field='dog',
            combine='and', value='jeff', query_type='Contains'
        )
        query = queries.DatabaseQuery(self.user, [criteria_1, criteria_2])
        exp = """
testuser (01/12/2017 10:10:00)
Searching for:
Wearer of Hats Name contains jeff
and Hound Owner Hound contains jeff
""".strip()
        self.assertEqual(exp, query.description())

    def test_episodes_for_m2m_fields(self):
        criteria = dict(
            rule='hat_wearer', field='hats',
            combine='and', value='Bowler', query_type='Equals'
        )

        bowler = testmodels.Hat(name='Bowler')
        bowler.save()

        hatwearer = testmodels.HatWearer(episode=self.episode)
        hatwearer.save()
        hatwearer.hats.add(bowler)
        hatwearer.save()

        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_m2m_fields_equals_with_synonyms(self):
        criteria = dict(
            rule='hat_wearer', field='hats',
            combine='and', value='Derby', query_type='Equals'
        )

        bowler = testmodels.Hat.objects.create(name='Bowler')
        content_type = ContentType.objects.get_for_model(testmodels.Hat)
        Synonym.objects.get_or_create(
            content_type=content_type,
            object_id=bowler.id,
            name="Derby"
        )

        hatwearer = testmodels.HatWearer(episode=self.episode)
        hatwearer.save()
        hatwearer.hats.add(bowler)
        hatwearer.save()

        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_m2m_fields_contains_synonym_and_name(self):
        criteria = dict(
            rule='hat_wearer', field='hats',
            combine='and', value='Der', query_type='Contains'
        )

        bowler = testmodels.Hat.objects.create(name='Bowler')
        content_type = ContentType.objects.get_for_model(testmodels.Hat)
        Synonym.objects.get_or_create(
            content_type=content_type,
            object_id=bowler.id,
            name="Derby"
        )

        hatwearer = testmodels.HatWearer(episode=self.episode)
        hatwearer.save()
        hatwearer.hats.add(bowler)
        hatwearer.save()

        # now we add another episode with an actual hat
        derbishire = testmodels.Hat.objects.create(name='derbishire')
        _, other_episode = self.new_patient_and_episode_please()

        hatwearer = testmodels.HatWearer(episode=other_episode)
        hatwearer.save()
        hatwearer.hats.add(derbishire)
        hatwearer.save()

        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode, other_episode], query.get_episodes())

    def test_fuzzy_query(self):
        """ It should return the patients that
            match the criteria ordered in by
            their related episode id descending
        """
        patient_1, episode_1 = self.new_patient_and_episode_please()
        patient_2, episode_2 = self.new_patient_and_episode_please()
        patient_3, episode_3 = self.new_patient_and_episode_please()
        models.Demographics.objects.filter(
            patient__in=[patient_1, patient_2, patient_3]
        ).update(
            first_name="tree"
        )
        patient_2.create_episode()
        # this patient, episode should not be found
        self.new_patient_and_episode_please()
        query = queries.DatabaseQuery(self.user, "tree")
        patients = query.fuzzy_query()

        # expectation is that patient 2 comes last as
        # they have the most recent episode
        self.assertEqual(
            list(patients),
            [patient_2, patient_3, patient_1]
        )

    def test_get_patients(self):
        patient_1, episode_1 = self.new_patient_and_episode_please()
        patient_2, episode_2 = self.new_patient_and_episode_please()
        episode_3 = patient_1.create_episode()

        # these will not be used
        self.new_patient_and_episode_please()

        query = queries.DatabaseQuery(self.user, [self.name_criteria])
        with patch.object(query, "get_episodes") as get_episodes:
            get_episodes.return_value = Episode.objects.filter(
                id__in=[episode_1.id, episode_2.id, episode_3.id]
            )
            found = query.get_patients().values_list("id", flat=True)
            self.assertEqual(
                2, found.count()
            )
            self.assertEqual(
                found[0], patient_1.id
            )
            self.assertEqual(
                found[1], patient_2.id
            )

    def test_distinct_episodes_for_m2m_fields_containing_synonsyms_and_names(
        self
    ):
        criteria = dict(
            rule='hat_wearer', field='hats',
            combine='and', value='Der', query_type='Contains'
        )

        bowler = testmodels.Hat.objects.create(name='Bowler')
        content_type = ContentType.objects.get_for_model(testmodels.Hat)
        Synonym.objects.get_or_create(
            content_type=content_type,
            object_id=bowler.id,
            name="Derby"
        )

        hatwearer = testmodels.HatWearer(episode=self.episode)
        hatwearer.save()
        hatwearer.hats.add(bowler)
        hatwearer.save()

        derbishire = testmodels.Hat.objects.create(name='derbishire')
        hatwearer.hats.add(derbishire)
        hatwearer.save()

        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_m2m_fields_patient_subrecord(self):
        criteria = dict(
            rule='favourite_dogs', field='dogs',
            combine='and', value='Dalmation', query_type='Equals'
        )

        dalmation = testmodels.Dog(name='Dalmation')
        dalmation.save()

        favouritedogs = testmodels.FavouriteDogs.objects.create(
            patient=self.patient
        )

        favouritedogs.dogs.add(dalmation)
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_fkorft_fields_for_patient_subrecord(self):
        criteria = dict(
            rule='demographics', field='sex',
            combine='and', value='Unknown', query_type='Equals'
        )
        unknown = Gender(name='Unknown')
        unknown.save()
        demographics = self.patient.demographics_set.first()
        demographics.sex = 'Unknown'
        demographics.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_fkorft_fields_for_patient_subrecord_with_multiple_episodes(self):
        criteria = dict(
            rule='demographics', field='sex',
            combine='and', value='Unknown', query_type='Equals'
        )
        unknown = Gender(name='Unknown')
        unknown.save()
        demographics = self.patient.demographics_set.first()
        demographics.sex = 'Unknown'
        demographics.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_for_fkorft_fields_exact_episode_subrecord(self):
        criteria = dict(
            rule='hound_owner', field='dog',
            combine='and', value='Dalmation', query_type='Equals'
        )

        dalmation = testmodels.Dog(name='Dalmation')
        dalmation.save()

        hound_owner = testmodels.HoundOwner.objects.create(
            episode=self.episode
        )
        hound_owner.dog = "Dalmation"
        hound_owner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episode_for_exact_fkorft_synonym(self):
        criteria = dict(
            rule='hound_owner', field='dog',
            combine='and', value='Dalmation', query_type='Equals'
        )

        spotted_dog = testmodels.Hat.objects.create(name='Spotted Dog')
        content_type = ContentType.objects.get_for_model(testmodels.Hat)
        Synonym.objects.get_or_create(
            content_type=content_type,
            object_id=spotted_dog.id,
            name="Dalmation"
        )

        hound_owner = testmodels.HoundOwner.objects.create(
            episode=self.episode
        )
        hound_owner.dog = "Dalmation"
        hound_owner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episode_for_exact_fkorft_free_text(self):
        criteria = dict(
            rule='hound_owner', field='dog',
            combine='and', value='dalmation', query_type='Equals'
        )

        hound_owner = testmodels.HoundOwner.objects.create(
            episode=self.episode
        )
        hound_owner.dog = "Dalmation"
        hound_owner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episode_for_fkorft_fields_contains_episode_subrecord(self):
        criteria = dict(
            rule='hound_owner', field='dog',
            combine='and', value='dal', query_type='Contains'
        )

        dalmation = testmodels.Dog(name='Dalmation')
        dalmation.save()

        hound_owner = testmodels.HoundOwner.objects.create(
            episode=self.episode
        )
        hound_owner.dog = "Dalmation"
        hound_owner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episode_fkorft_for_contains_synonym(self):
        criteria = dict(
            rule='hound_owner', field='dog',
            combine='and', value='dal', query_type='Contains'
        )

        spotted_dog = testmodels.Dog.objects.create(name='Spotted Dog')
        content_type = ContentType.objects.get_for_model(testmodels.Dog)
        Synonym.objects.get_or_create(
            content_type=content_type,
            object_id=spotted_dog.id,
            name="Dalmation"
        )

        hound_owner = testmodels.HoundOwner.objects.create(
            episode=self.episode
        )
        hound_owner.dog = "Dalmation"
        hound_owner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episode_fkorft_for_contains_ft(self):
        criteria = dict(
            rule='hound_owner', field='dog',
            combine='and', value='dal', query_type='Contains'
        )

        hound_owner = testmodels.HoundOwner.objects.create(
            episode=self.episode
        )
        hound_owner.dog = "Dalmation"
        hound_owner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode], query.get_episodes())

    def test_episode_fkorft_for_contains_synonym_name_and_ft(self):
        criteria = dict(
            rule='hound_owner', field='dog',
            combine='and', value='dal', query_type='Contains'
        )

        spotted_dog = testmodels.Dog.objects.create(name='Spotted Dog')
        content_type = ContentType.objects.get_for_model(testmodels.Dog)
        Synonym.objects.get_or_create(
            content_type=content_type,
            object_id=spotted_dog.id,
            name="Dalmation"
        )

        hound_owner = testmodels.HoundOwner.objects.create(
            episode=self.episode
        )
        hound_owner.dog = "Dalmation"
        hound_owner.save()

        _, episode_2 = self.new_patient_and_episode_please()
        hound_owner = testmodels.HoundOwner.objects.create(
            episode=episode_2
        )
        hound_owner.dog = "Dalwinion"
        hound_owner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode, episode_2], query.get_episodes())

    def test_episode_fkorft_contains_distinct(self):
        criteria = dict(
            rule='hound_owner', field='dog',
            combine='and', value='dal', query_type='Contains'
        )

        spotted_dog = testmodels.Dog.objects.create(name='Spotted Dog')
        content_type = ContentType.objects.get_for_model(testmodels.Dog)
        Synonym.objects.get_or_create(
            content_type=content_type,
            object_id=spotted_dog.id,
            name="Dalmation"
        )

        hound_owner = testmodels.HoundOwner.objects.create(
            episode=self.episode
        )
        hound_owner.dog = "Dalmation"
        hound_owner.save()
        episode_2 = self.patient.create_episode()

        hound_owner = testmodels.HoundOwner.objects.create(
            episode=episode_2
        )
        hound_owner.dog = "Dalwinion"
        hound_owner.save()
        query = queries.DatabaseQuery(self.user, [criteria])
        self.assertEqual([self.episode, episode_2], query.get_episodes())

    def test_episodes_for_criteria_episode_subrecord_string_field(self):
        criteria = [
            {
                u'rule': u'hat_wearer',
                u'field': u'name',
                u'combine': u'and',
                u'value': u'Bowler',
                u'query_type': u'Equals'
            }
        ]
        query = queries.DatabaseQuery(self.user, criteria)
        res = query.episodes_for_criteria(criteria[0])
        self.assertEqual([], list(res))

    def test_episodes_for_criteria_search_rule_used(self):
        criteria = [
            {
                u'rule': u'hat_wearer',
                u'field': u'Name',
                u'combine': u'and',
                u'value': u'Bowler',
                u'query_type': u'Equals'
            }
        ]

        class HatWearerQuery(object):
            def query(self, given_query):
                pass

        with patch.object(SearchRule, "get_rule") as search_rule_get:
            with patch.object(HatWearerQuery, "query") as hat_wearer_query:
                search_rule_get.return_value = HatWearerQuery
                query = queries.DatabaseQuery(self.user, criteria)
                query.episodes_for_criteria(criteria[0])
                search_rule_get.assert_called_once_with(
                    "hat_wearer", self.user
                )
                hat_wearer_query.assert_called_once_with(criteria[0])

    def test_episodes_without_restrictions_no_matches(self):
        query = queries.DatabaseQuery(self.user, self.name_criteria)
        self.episode.delete()
        query.value = []
        result = query._episodes_without_restrictions()
        self.assertEqual(set([]), result)

    def test_episodes_without_restrictions(self):
        query = queries.DatabaseQuery(self.user, self.name_criteria)
        result = query._episodes_without_restrictions()
        self.assertEqual(self.episode, list(result)[0])

    def test_filter_restricted_only_user(self):
        self.user.profile.restricted_only = True
        self.user.profile.save()
        self.patient.create_episode()
        query = queries.DatabaseQuery(self.user, self.name_criteria)
        self.assertEqual([], query.get_episodes())

    def test_filter_in_restricted_episode_types(self):
        self.user.profile.restricted_only = True
        self.user.profile.save()
        episode2 = self.patient.create_episode(category_name='Restricted')
        self.assertEqual('Restricted', episode2.category_name)

        query = queries.DatabaseQuery(self.user, self.name_criteria)
        self.assertEqual([episode2], query.get_episodes())

    def test_get_episodes(self):
        query = queries.DatabaseQuery(self.user, self.name_criteria)
        self.assertEqual([self.episode], query.get_episodes())

    def test_get_episodes_multi_query(self):
        criteria = [
            {
                u'rule': u'demographics',
                u'field': u'sex',
                u'combine': u'and',
                u'value': u'Female',
                u'query_type': u'Equals'
            },
            self.name_criteria[0]
        ]
        query = queries.DatabaseQuery(self.user, criteria)
        self.assertEqual([self.episode], query.get_episodes())

    def test_get_episodes_searching_ft_or_fk_field(self):
        criteria = [
            {
                u'rule': u'demographics',
                u'field': u'sex',
                u'combine': u'and',
                u'value': u'Female',
                u'query_type': u'Equals'
            }
        ]
        query = queries.DatabaseQuery(self.user, criteria)
        self.assertEqual([self.episode], query.get_episodes())

    def test_episodes_searching_fk_or_ft_fields_with_synonym_values(self):
        criteria = [
            {
                u'rule': u'demographics',
                u'field': u'sex',
                u'combine': u'and',
                u'value': u'F',
                u'query_type': u'Equals'
            }
        ]
        female = Gender.objects.create(name="Female")
        ct = ContentType.objects.get_for_model(Gender)
        Synonym.objects.create(content_type=ct, name="F", object_id=female.id)
        demographics = self.patient.demographics_set.get()
        demographics.sex = "F"
        demographics.save()
        self.assertEqual("Female", demographics.sex)
        query = queries.DatabaseQuery(self.user, criteria)
        self.assertEqual([self.episode], query.get_episodes())

    def test_get_episodes_searching_episode_subrecord_ft_or_fk_fields(self):
        criteria = [
            {
                u'rule': u'dog_owner',
                u'field': u'dog',
                u'combine': u'and',
                u'value': u'Terrier',
                u'query_type': u'Equals'
            }
        ]
        dog_owner = testmodels.DogOwner.objects.create(episode=self.episode)
        dog_owner.dog = 'Terrier'
        dog_owner.save()
        query = queries.DatabaseQuery(self.user, criteria)
        self.assertEqual([self.episode], query.get_episodes())

    def test_get_patient_summaries(self):
        query = queries.DatabaseQuery(self.user, self.name_criteria)
        summaries = query.get_patient_summaries(Patient.objects.all())
        expected = [{
            'count': 1,
            'hospital_number': u'0',
            'date_of_birth': self.DATE_OF_BIRTH,
            'first_name': u'Sally',
            'surname': u'Stevens',
            'end': self.DATE_OF_EPISODE,
            'start': self.DATE_OF_EPISODE,
            'patient_id': 1,
            'categories': [u'Inpatient']
        }]
        self.assertEqual(expected, summaries)

    def test_get_patient_summaries_for_patient_with_multiple_episodes(self):
        """ with a patient with multiple episodes
            we expect it to aggregate these into summaries
        """
        start_date = date(day=1, month=2, year=2014)
        self.patient.create_episode(
            start=start_date
        )
        end_date = date(day=1, month=2, year=2016)
        self.patient.create_episode(
            end=end_date
        )
        query = queries.DatabaseQuery(self.user, self.name_criteria)
        summaries = query.get_patient_summaries(Patient.objects.all())
        expected = [{
            'count': 3,
            'hospital_number': u'0',
            'date_of_birth': self.DATE_OF_BIRTH,
            'first_name': u'Sally',
            'surname': u'Stevens',
            'end': end_date,
            'start': start_date,
            'patient_id': 1,
            'categories': [u'Inpatient']
        }]
        self.assertEqual(expected, summaries)


class CreateQueryTestCase(OpalTestCase):

    @patch('search.queries.stringport')
    def test_from_settings(self, stringport):
        mock_backend = MagicMock('Mock Backend')
        stringport.return_value = mock_backend

        with self.settings(OPAL_SEARCH_BACKEND='mybackend'):
            backend = queries.create_query(self.user, [])
            self.assertEqual(mock_backend.return_value, backend)
            mock_backend.assert_called_with(self.user, [])
