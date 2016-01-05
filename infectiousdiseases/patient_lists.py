from opal.core.patient_lists import PatientList, TaggedPatientList
from elcid import models


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


class Microbiology(TaggedPatientList):
    tag = "microbiology"
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

    schema = [
        models.Demographics,
        models.Location,
        models.Diagnosis,
        models.PastMedicalHistory,
        models.Travel,
        models.Antimicrobial,
        models.MicrobiologyTest,
        models.GeneralNote,
        models.Todo,
        ]
