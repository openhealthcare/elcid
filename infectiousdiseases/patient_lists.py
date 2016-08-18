from opal.core.patient_lists import PatientList, TaggedPatientList
from elcid import models

generic_infectious_diseases_list = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.GeneralNote,
    models.Todo
]


class Virology(TaggedPatientList):
    display_name = 'Virology'
    tag = "virology"
    order = 7
    schema = [
        models.Demographics,
        models.Location,
        models.Diagnosis,
        models.Antimicrobial,
        models.MicrobiologyTest,
        models.MicrobiologyInput,
        models.GeneralNote
    ]


class MicroOrtho(TaggedPatientList):
    display_name = 'Micro Ortho'
    tag = "microbiology"
    subtag = "micro_ortho"
    order = 6
    schema = [
        models.Demographics,
        models.Location,
        models.Diagnosis,
        models.Antimicrobial,
        models.MicrobiologyTest,
        models.MicrobiologyInput,
        models.GeneralNote
    ]


class InfectiousDiseasesIdLiason(TaggedPatientList):
    display_name = 'ID Liaison'
    tag = "infectious_diseases"
    subtag = "id_liaison"
    order = 2

    schema = [
        models.Demographics,
        models.Location,
        models.Diagnosis,
        models.PastMedicalHistory,
        models.Antimicrobial,
        models.MicrobiologyTest,
        models.MicrobiologyInput,
        models.GeneralNote,
        models.Todo
    ]


class InfectiousDiseasesIdInpatient(TaggedPatientList):
    display_name = 'ID Inpatients'
    tag = "infectious_diseases"
    subtag = "id_inpatients"
    order = 1

    schema = generic_infectious_diseases_list


class ImmuneInpatients(TaggedPatientList):
    display_name = 'Immune Inpatients'
    tag = "hiv"
    subtag = "immune_inpatients"
    order = 3

    schema = generic_infectious_diseases_list


class ImmuneLiason(TaggedPatientList):
    display_name = 'Immune Liaison'
    tag = "hiv"
    subtag = "immune_liason"
    order = 4

    schema = generic_infectious_diseases_list


class Tropical(TaggedPatientList):
    display_name = 'Tropical'
    tag = "tropical_diseases"
    schema = generic_infectious_diseases_list
    order = 5


class Weekend(PatientList):
    """
    On the weekend a single team handles the work of three regular teams.
    """
    display_name = 'Weekend HTD'
    order = 99
    schema = generic_infectious_diseases_list

    def get_queryset(self):
        from opal.models import Episode # Avoid circular import from opal.models
        return Episode.objects.filter(
            tagging__archived=False,
            tagging__value__in=[
                'tropical_diseases', 'immune_inpatients', 'id_inpatients'
            ]
        )
