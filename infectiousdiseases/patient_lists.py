from opal.core.patient_lists import TaggedPatientList
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
    tag = "virology"
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
    tag = "microbiology"
    subtag = "micro_ortho"
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
    tag = "infectious_diseases"
    subtag = "id_liaison"

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
    tag = "infectious_diseases"
    subtag = "id_inpatients"

    schema = generic_infectious_diseases_list


class ImmuneInpatients(TaggedPatientList):
    tag = "hiv"
    subtag = "immune_inpatients"

    schema = generic_infectious_diseases_list


class ImmuneLiason(TaggedPatientList):
    tag = "hiv"
    subtag = "immune_liason"

    schema = generic_infectious_diseases_list


class Tropical(TaggedPatientList):
    tag = "tropical_diseases"
    schema = generic_infectious_diseases_list
