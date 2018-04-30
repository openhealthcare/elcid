"""
Unittests for search.extract
"""
import datetime
import os
# from collections import OrderedDict
#
from mock import mock_open, patch
from functools import partial
from search import extract, extract_serializers
from search.exceptions import SearchException
from elcid import models as emodels
from opal.core.test import OpalTestCase
from opal import models
from opal.tests import models as tmodels
from six import u, b  # NOQA


MOCKING_FILE_NAME_OPEN = "search.extract.open"


class AbstractExtractTestCase(OpalTestCase):
    @patch("search.extract.csv.writer")
    @patch("search.extract.write_data_dictionary")
    def mock_extract(
        self,
        generate_nested_csv_extract,
        write_data_dictionary,
        writer
    ):
        """ Mocks up the nested extract so that there
            are no side effects, pass through a partial
            of the call you want to test, get back
            what is written to csv_writer.write_row
        """
        m = mock_open()
        with patch(MOCKING_FILE_NAME_OPEN, m, create=True):
            generate_nested_csv_extract()
        call_args = writer().writerow.call_args_list
        return [i[0][0] for i in call_args]

    def get_nested_extract(self, episodes, field_dict):
        p = partial(
            extract.generate_nested_csv_extract,
            "",  # not used
            episodes,
            self.user,
            field_dict
        )
        return self.mock_extract(p)

    def get_multi_file_extract(self, episodes, serializers):
        p = partial(
            extract.generate_multi_csv_extract,
            "",  # not used
            episodes,
            self.user
        )
        with patch("search.extract.ExtractSerializer.list") as l:
            l.return_value = serializers
            result = self.mock_extract(p)

        return result

    def get_write_description(self, episodes, fields=None):
        m = mock_open()
        with patch(MOCKING_FILE_NAME_OPEN, m, create=True):
            extract.write_description(
                episodes,
                self.user,
                "some_description",
                "some_dir",
                fields=fields
            )
            call_args = m().write.call_args
        return call_args[0][0]


class NestedEpisodeTestCase(AbstractExtractTestCase):
    def test_nested_csv_extract_episode_start(self):
        """ A simple initial test that just
            says, give me all episode start dates
        """
        _, episode = self.new_patient_and_episode_please()
        episode.start = datetime.date(2018, 2, 1)
        episode.save()
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            {"episode": ["start"]}
        )
        self.assertEqual(result[0], ["Episode Start"])
        self.assertEqual(result[1], ["2018-02-01"])

    def test_nested_csv_extract_without_episode_start(self):
        _, _ = self.new_patient_and_episode_please()
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            {"episode": ["start"]}
        )
        self.assertEqual(result[0], ["Episode Start"])
        self.assertEqual(result[1], [""])


class NestedEpisodeSubrecordTestCase(AbstractExtractTestCase):

    def test_nested_csv_extract(self):
        """ a nested subrecord with an episode subrecord
        """
        field_dict = {
            emodels.GeneralNote.get_api_name(): ["comment"]
        }
        _, episode = self.new_patient_and_episode_please()
        emodels.GeneralNote.objects.create(
            episode=episode, comment="This will need to be searched"
        )
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(result[0], ["General Notes Comment"])
        self.assertEqual(result[1], ["This will need to be searched"])

    def test_nested_csv_extract_multi_field(self):
        field_dict = {
            emodels.GeneralNote.get_api_name(): ["comment", "date"]
        }
        _, episode = self.new_patient_and_episode_please()
        emodels.GeneralNote.objects.create(
            episode=episode,
            comment="This will need to be searched",
            date=datetime.date(2018, 2, 1)
        )
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0],
            ["General Notes Comment", "General Notes Date"]
        )
        self.assertEqual(
            result[1],
            ["This will need to be searched", "2018-02-01"]
        )

    def test_nested_csv_extract_multiple_episode_subrecords_same_episode(self):
        field_dict = {
            emodels.GeneralNote.get_api_name(): ["comment"]
        }
        _, episode = self.new_patient_and_episode_please()
        emodels.GeneralNote.objects.create(
            episode=episode, comment="This will need to be searched"
        )
        emodels.GeneralNote.objects.create(
            episode=episode, comment="This will also need to be searched"
        )
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0],
            ['General Notes 1 Comment', 'General Notes 2 Comment']
        )

        self.assertEqual(
            result[1],
            [
                "This will need to be searched",
                "This will also need to be searched"
            ]
        )

    def test_with_non_asci_charecters(self):
        field_dict = {
            emodels.GeneralNote.get_api_name(): ["comment"]
        }
        comment = u("\u0160\u0110\u0106\u017d\u0107\u017e\u0161\u0111")
        _, episode = self.new_patient_and_episode_please()
        emodels.GeneralNote.objects.create(
            episode=episode, comment=comment
        )
        expected = [
            b"\xc5\xa0\xc4\x90\xc4\x86\xc5\xbd\xc4\x87\xc5\xbe\xc5\xa1\xc4\x91"
        ]
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[1],
            expected
        )

    def test_with_fk_or_ft_fk(self):
        """
            Check that renderers work with fk_or_ft fk fields
        """
        _, episode = self.new_patient_and_episode_please()
        models.Condition.objects.create(
            name="cough"
        )
        pmh = emodels.PastMedicalHistory.objects.create(
            episode=episode
        )
        pmh.condition = "cough"
        pmh.save()
        self.assertIsNotNone(pmh.condition_fk_id)
        field_dict = {
            emodels.PastMedicalHistory.get_api_name(): ["condition"]
        }
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], ["PMH Condition"]
        )
        self.assertEqual(
            result[1], ["cough"]
        )

    def test_with_fk_or_ft_ft(self):
        _, episode = self.new_patient_and_episode_please()

        pmh = emodels.PastMedicalHistory.objects.create(
            episode=episode
        )
        pmh.condition = "cough"
        pmh.save()
        self.assertIsNotNone(pmh.condition_ft)
        field_dict = {
            emodels.PastMedicalHistory.get_api_name(): ["condition"]
        }
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], ["PMH Condition"]
        )
        self.assertEqual(
            result[1], ["cough"]
        )

    def test_with_multiple_episode_subrecords(self):
        _, episode = self.new_patient_and_episode_please()
        field_dict = {
            emodels.GeneralNote.get_api_name(): ["comment"],
            emodels.Travel.get_api_name(): ["destination"]
        }
        emodels.GeneralNote.objects.create(
            episode=episode, comment="This will need to be searched"
        )
        emodels.Travel.objects.create(
            episode=episode, destination_ft="France"
        )
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], ['Travel Destination', 'General Notes Comment']
        )
        self.assertEqual(
            result[1], ["France", "This will need to be searched"]
        )

    def test_with_multiple_episode_subrecords_across_episodes(self):
        _, episode_1 = self.new_patient_and_episode_please()
        _, episode_2 = self.new_patient_and_episode_please()
        field_dict = {
            emodels.GeneralNote.get_api_name(): ["comment"],
            emodels.Travel.get_api_name(): ["destination"]
        }
        emodels.GeneralNote.objects.create(
            episode=episode_1, comment="This will need to be searched"
        )
        emodels.Travel.objects.create(
            episode=episode_1, destination_ft="France"
        )
        emodels.GeneralNote.objects.create(
            episode=episode_2, comment="This will also need to be searched"
        )
        emodels.Travel.objects.create(
            episode=episode_2, destination_ft="Germany"
        )
        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], ['Travel Destination', 'General Notes Comment']
        )
        self.assertEqual(
            result[1], ["France", "This will need to be searched"]
        )
        self.assertEqual(
            result[2], ["Germany", "This will also need to be searched"]
        )

    def test_with_multiple_episodes_where_some_subrecords_are_none(self):
        _, episode_1 = self.new_patient_and_episode_please()
        _, episode_2 = self.new_patient_and_episode_please()
        field_dict = {
            emodels.GeneralNote.get_api_name(): ["comment"],
            emodels.Travel.get_api_name(): ["destination"]
        }

        emodels.Travel.objects.create(
            episode=episode_1, destination_ft="France"
        )
        emodels.GeneralNote.objects.create(
            episode=episode_2, comment="This will also need to be searched"
        )

        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], ['Travel Destination', 'General Notes Comment']
        )
        self.assertEqual(
            result[1], ["France", ""]
        )
        self.assertEqual(
            result[2], ["", "This will also need to be searched"]
        )

    def test_with_some_episodes_that_are_not_required(self):
        _, episode_1 = self.new_patient_and_episode_please()
        _, episode_2 = self.new_patient_and_episode_please()
        field_dict = {
            emodels.GeneralNote.get_api_name(): ["comment"],
            emodels.Travel.get_api_name(): ["destination"]
        }

        emodels.Travel.objects.create(
            episode=episode_1, destination_ft="France"
        )
        emodels.GeneralNote.objects.create(
            episode=episode_2, comment="This will also need to be searched"
        )

        result = self.get_nested_extract(
            models.Episode.objects.exclude(id=episode_2.id),
            field_dict
        )
        self.assertEqual(
            result[0], ['Travel Destination', 'General Notes Comment']
        )
        self.assertEqual(
            result[1], ["France", ""]
        )
        self.assertEqual(len(result), 2)


class NestedPatientSubrecordTestCase(AbstractExtractTestCase):
    def test_with_a_single_patient(self):
        patient, _ = self.new_patient_and_episode_please()
        field_dict = {
            emodels.Allergies.get_api_name(): ["drug"],
        }
        emodels.Allergies.objects.create(
            drug_ft="Penicillin", patient=patient
        )

        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], ['Allergies Drug']
        )
        self.assertEqual(
            result[1], ["Penicillin"]
        )

    def test_with_a_single_patient_with_multiple_episodes(self):
        patient, _ = self.new_patient_and_episode_please()
        patient.create_episode()
        field_dict = {
            emodels.Allergies.get_api_name(): ["drug"],
        }
        emodels.Allergies.objects.create(
            drug_ft="Penicillin", patient=patient
        )

        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], ['Allergies Drug']
        )
        self.assertEqual(
            result[1], ["Penicillin"]
        )
        self.assertEqual(
            result[2], ["Penicillin"]
        )

    def test_with_a_single_patient_where_some_episodes_are_excluded(self):
        patient, episode = self.new_patient_and_episode_please()
        patient.create_episode()
        field_dict = {
            emodels.Allergies.get_api_name(): ["drug"],
        }
        emodels.Allergies.objects.create(
            drug_ft="Penicillin", patient=patient
        )

        result = self.get_nested_extract(
            models.Episode.objects.exclude(id=episode.id),
            field_dict
        )
        self.assertEqual(
            result[0], ['Allergies Drug']
        )
        self.assertEqual(
            result[1], ["Penicillin"]
        )

    def test_with_multiple_patients(self):
        patient_1, episode_1 = self.new_patient_and_episode_please()
        patient_2, episode_2 = self.new_patient_and_episode_please()
        field_dict = {
            emodels.Allergies.get_api_name(): ["drug"],
        }
        emodels.Allergies.objects.create(
            drug_ft="Penicillin", patient=patient_1
        )
        emodels.Allergies.objects.create(
            drug_ft="Aspirin", patient=patient_2
        )

        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], ['Allergies Drug']
        )
        self.assertEqual(
            result[1], ["Penicillin"]
        )
        self.assertEqual(
            result[2], ["Aspirin"]
        )


class NestedMixedTestCase(AbstractExtractTestCase):
    def test_nested_episode_and_patient_subrecords(self):
        patient, episode_1 = self.new_patient_and_episode_please()
        episode_1.start = datetime.date(2018, 01, 03)
        episode_1.save()
        episode_2 = patient.create_episode()
        episode_2.start = datetime.date(2018, 02, 03)
        episode_2.save()

        field_dict = {
            emodels.Allergies.get_api_name(): ["drug"],
            emodels.GeneralNote.get_api_name(): ["comment"],
            "episode": ["start"]
        }
        emodels.Allergies.objects.create(
            drug_ft="Penicillin", patient=patient
        )
        emodels.GeneralNote.objects.create(
            episode=episode_1, comment="So this is one episode"
        )
        emodels.GeneralNote.objects.create(
            episode=episode_2, comment="So this is another episode"
        )

        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], [
                'Allergies Drug', 'General Notes Comment', 'Episode Start'
            ]
        )
        self.assertEqual(
            result[1],
            ['Penicillin', 'So this is one episode', '2018-01-03']
        )
        self.assertEqual(
            result[2],
            ['Penicillin', 'So this is another episode', '2018-02-03']
        )

    def test_nested_where_some_fields_are_none(self):
        patient, episode_1 = self.new_patient_and_episode_please()
        episode_1.start = datetime.date(2018, 01, 03)
        episode_1.save()
        episode_2 = patient.create_episode()

        # add an additionl episode
        patient.create_episode()

        field_dict = {
            emodels.Allergies.get_api_name(): ["drug"],
            emodels.GeneralNote.get_api_name(): ["comment"],
            "episode": ["start"]
        }
        emodels.Allergies.objects.create(
            drug_ft="Penicillin", patient=patient
        )
        emodels.GeneralNote.objects.create(
            episode=episode_2, comment="So this is another episode"
        )

        result = self.get_nested_extract(
            models.Episode.objects.all(),
            field_dict
        )
        self.assertEqual(
            result[0], [
                'Allergies Drug', 'General Notes Comment', 'Episode Start'
            ]
        )
        self.assertEqual(
            result[1],
            ['Penicillin', '', '2018-01-03']
        )
        self.assertEqual(
            result[2],
            ['Penicillin', 'So this is another episode', '']
        )
        self.assertEqual(
            result[3],
            ['Penicillin', '', '']
        )

    def test_nested_where_some_episodes_are_excluded(self):
        patient_1, episode_1 = self.new_patient_and_episode_please()
        episode_1.start = datetime.date(2018, 01, 03)
        episode_1.save()
        episode_2 = patient_1.create_episode()

        patient_2, episode_3 = self.new_patient_and_episode_please()
        field_dict = {
            emodels.Allergies.get_api_name(): ["drug"],
            emodels.GeneralNote.get_api_name(): ["comment"],
            "episode": ["start"]
        }
        emodels.Allergies.objects.create(
            drug_ft="Penicillin", patient=patient_1
        )
        emodels.GeneralNote.objects.create(
            episode=episode_2, comment="So this is another episode"
        )
        emodels.Allergies.objects.create(
            drug_ft="Aspirin", patient=patient_2
        )

        result = self.get_nested_extract(
            models.Episode.objects.exclude(id=episode_1.id),
            field_dict
        )

        self.assertEqual(
            len(result), 3
        )
        self.assertEqual(
            result[0], [
                'Allergies Drug', 'General Notes Comment', 'Episode Start'
            ]
        )
        self.assertEqual(
            result[1],
            ['Penicillin', 'So this is another episode', '']
        )
        self.assertEqual(
            result[2],
            ['Aspirin', '', '']
        )


class NotAdvancedSearchableNestedTestCase(AbstractExtractTestCase):
    @patch.object(emodels.PrimaryDiagnosis, "_get_fieldnames_to_extract")
    def test_excludes_not_advanced_searchable_fields(self, gfe):
        gfe.return_value = ["condition"]
        field_dict = {
            emodels.PrimaryDiagnosis.get_api_name(): ["condition", "confirmed"]
        }
        _, episode = self.new_patient_and_episode_please()
        primary_diagnosis = emodels.PrimaryDiagnosis.objects.create(
            episode=episode, confirmed=True
        )
        primary_diagnosis.condition = "cough"
        primary_diagnosis.save()
        with self.assertRaises(SearchException) as se:
            self.get_nested_extract(
                models.Episode.objects.all(),
                field_dict
            )
        self.assertEqual(
            str(se.exception),
            "Unable to find field confirmed for Primary Diagnosis"
        )


class MultiFileCsvExtractTestCase(AbstractExtractTestCase):
    def test_multi_csv_extract_for_episode_subrecords(self):
        _, episode = self.new_patient_and_episode_please()
        episode.start = datetime.date(2018, 2, 1)
        api_name = emodels.GeneralNote.get_api_name()
        emodels.GeneralNote.objects.create(
            comment="This is interesting",
            episode=episode
        )
        result = self.get_multi_file_extract(
            models.Episode.objects.all(),
            [extract_serializers.ExtractSerializer.get(api_name, self.user)]
        )
        general_note_fields = [
            u'Created',
            u'Updated',
            u'Created By',
            u'Updated By',
            u'Episode',
            u'Date',
            u'Comment'
        ]
        self.assertEqual(
            result[0],
            general_note_fields
        )
        expected_result = [
            '', '', '', '', '1', '', 'This is interesting'
        ]

        self.assertEqual(
            result[1],
            expected_result
        )
        self.assertEqual(len(result), 2)

    def test_multi_csv_extract_for_episode(self):
        _, episode = self.new_patient_and_episode_please()
        episode.start = datetime.date(2018, 2, 1)
        episode.save()
        result = self.get_multi_file_extract(
            models.Episode.objects.all(),
            [extract_serializers.ExtractSerializer.get("episode", self.user)]
        )
        expected_result = [
            '', '2018-02-01', '', '', '', '', ''
        ]
        expected_headers = [
            'Team',
            'Start',
            'End',
            'Created',
            'Updated',
            'Created By',
            'Updated By',
        ]

        self.assertEqual(
            result[0],
            expected_headers
        )

        self.assertEqual(
            result[1],
            expected_result
        )
        self.assertEqual(len(result), 2)

    def test_mutli_csv_extract_for_patient_subrecords(self):
        patient, _ = self.new_patient_and_episode_please()
        api_name = emodels.Allergies.get_api_name()
        allergy = emodels.Allergies.objects.create(
            patient=patient
        )
        allergy.drug = "Penicillin"
        allergy.save()
        api_name = emodels.Allergies.get_api_name()
        result = self.get_multi_file_extract(
            models.Episode.objects.all(),
            [extract_serializers.ExtractSerializer.get(api_name, self.user)]
        )
        allergy_fields = [
            'External System',
            'External Identifier',
            'Created',
            'Updated',
            'Created By',
            'Updated By',
            'Patient',
            'Provisional',
            'Details',
            'Allergy Description',
            'Allergy Type Description',
            'Certainty Id',
            'Certainty Description',
            'Allergy Reference Name',
            'Allergen Reference System',
            'Allergen Reference',
            'Status Id',
            'Status Description',
            'Diagnosis Datetime',
            'Allergy Start Datetime',
            'No Allergies',
            'Drug'
        ]
        self.assertEqual(
            result[0],
            allergy_fields
        )
        expected_result = [
            '',
            '',
            '',
            '',
            '',
            '',
            '1',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            'False',
            'Penicillin'
        ]

        self.assertEqual(
            result[1],
            expected_result
        )
        self.assertEqual(len(result), 2)

    def test_ignores_empty_subrecords(self):
        _, episode = self.new_patient_and_episode_please()
        episode.start = datetime.date(2018, 2, 1)
        episode.save()

        api_name = emodels.GeneralNote.get_api_name()
        result = self.get_multi_file_extract(
            models.Episode.objects.all(),
            [
                extract_serializers.ExtractSerializer.get("episode", self.user),
                extract_serializers.ExtractSerializer.get(api_name, self.user)
            ]
        )
        expected_result = [
            '', '2018-02-01', '', '', '', '', ''
        ]
        expected_headers = [
            'Team',
            'Start',
            'End',
            'Created',
            'Updated',
            'Created By',
            'Updated By',
        ]

        self.assertEqual(
            result[0],
            expected_headers
        )

        self.assertEqual(
            result[1],
            expected_result
        )
        self.assertEqual(len(result), 2)


class WriteDescriptionTestCase(AbstractExtractTestCase):
    def test_with_fields(self):
        fields = dict(demographics=["birth_place", "death_indicator"])
        result = self.get_write_description(
            models.Episode.objects.all(), fields=fields
        )
        expected = "some_description \nExtracting:\nDemographics - \
Country of Birth, Death Indicator"
        self.assertEqual(
            result, expected
        )

    def test_with_fields_and_muiltiple_subrecords(self):
        fields = dict(
            demographics=["birth_place", "death_indicator"],
            location=["ward"]
        )
        result = self.get_write_description(
            models.Episode.objects.all(), fields=fields
        )
        expected = 'some_description \nExtracting:\nDemographics - Country of \
Birth, Death Indicator\nLocation - Ward'
        self.assertEqual(
            result, expected
        )

    def test_with_multiple_where_one_is_not_advanced_searchable(self):
        fields = dict(
            demographics=["birth_place", "death_indicator"],
            result=["lab_number"]
        )
        # Result is currently excluded from the extract
        result = self.get_write_description(
            models.Episode.objects.all(), fields=fields
        )

        expected = "some_description \nExtracting:\nDemographics - Country of Birth, \
Death Indicator"
        self.assertEqual(
            result, expected
        )

    def test_with_out_fields(self):
        fields = None
        # Result is currently excluded from the extract
        result = self.get_write_description(
            models.Episode.objects.all(), fields=fields
        )

        expected = "some_description"
        self.assertEqual(
            result, expected
        )


class ZipArchiveTestCase(OpalTestCase):
    @patch('search.extract.zipfile')
    @patch("search.extract.csv.writer")
    def get_zip_archive(self, episodes, fields, writer, zipfile):
        extract.zip_archive(
            models.Episode.objects.all(), 'this', self.user, fields=fields
        )
        z = zipfile.ZipFile.return_value.__enter__
        call_args = z.return_value.write.call_args_list
        files = {os.path.basename(i[0][0]) for i in call_args}
        writer_call_args = writer.call_args_list
        writer_files = {
            os.path.basename(i[0][0].name) for i in writer_call_args
        }
        return files.union(writer_files)

    def test_subrecords(self):
        patient, episode = self.new_patient_and_episode_please()

        tmodels.HatWearer.objects.create(name="Indiana", episode=episode)
        tmodels.HouseOwner.objects.create(patient=patient)
        base_names = self.get_zip_archive(models.Episode.objects.all(), None)
        expected = {
            "query.txt",
            "data_dictionary.html",
            "hat_wearer.csv",
            "house_owner.csv",
            "episode.csv"
        }
        self.assertEqual(base_names, expected)

    def test_subrecords_if_empty_query(self):
        # if there are no subrecords we don't expect them to write to the file
        file_names = self.get_zip_archive(models.Episode.objects.all(), None)
        self.assertEqual(3, len(file_names))
        self.assertEqual(
            file_names,
            set(['data_dictionary.html', 'episode.csv', 'query.txt'])
        )

    def test_nested_extract_called(self):
        fields = dict(episode=["start"])
        file_names = self.get_zip_archive(models.Episode.objects.all(), fields)
        self.assertEqual(3, len(file_names))
        self.assertEqual(
            file_names,
            set(['data_dictionary.html', 'extract.csv', 'query.txt'])
        )


class AsyncExtractTestCase(OpalTestCase):

    @patch('search.tasks.extract.delay')
    def test_async(self, delay):
        extract.async_extract(self.user, 'THIS')
        delay.assert_called_with(self.user, 'THIS')
