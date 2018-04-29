from opal.core.test import OpalTestCase
from search import subrecord_queries
from elcid import models


class BooleanTestCase(OpalTestCase):
    def test_boolean_true(self):
        model = models.Demographics
        field = "death_indicator"
        value = "true"
        patient, episode = self.new_patient_and_episode_please()
        patient.demographics_set.update(death_indicator=True)
        result = subrecord_queries.query_for_boolean_fields(
            model, field, value
        )
        self.assertEqual(
            list(result), list(patient.episode_set.all())
        )

    def test_boolean_false(self):
        model = models.Demographics
        field = "death_indicator"
        value = "true"
        patient, episode = self.new_patient_and_episode_please()
        patient.demographics_set.update(death_indicator=False)
        result = subrecord_queries.query_for_boolean_fields(
            model, field, value
        )
        self.assertEqual(
            list(result), []
        )
