"""
Patient Lists for the Walkin service
"""
from obs import models as obsmodels
from opal.core import patient_lists

from elcid import models

from walkin import models as wimodels

class WalkinDoctor(patient_lists.TaggedPatientList):
    display_name = 'Walkin Doctor'
    direct_add = False
    tag = "walkin"
    subtag = "walkin_doctor"
    order = 12
    schema = [
        models.Demographics,
        models.Location,
        models.Travel,
        wimodels.Symptom,
        wimodels.ClinicalFindings,
        models.MicrobiologyTest,
        models.Diagnosis,
        obsmodels.Observation,
        models.Antimicrobial,
        models.MicrobiologyInput
    ]


class WalkinNurseTriage(patient_lists.TaggedPatientList):
    display_name = 'Walkin Nurse Triage'
    direct_add = False
    tag = "walkin"
    subtag = "walkin_triage"
    order = 11
    schema = [
        models.Demographics,
        models.Location,
        models.Allergies,
        models.Travel,
        wimodels.Symptom,
        models.MicrobiologyTest,
        obsmodels.Observation,
    ]


class WalkinReview(patient_lists.TaggedPatientList):
    display_name = 'Walkin Review'
    direct_add = False
    tag = "walkin"
    subtag = "walkin_review"
    order = 13
    schema = [
        models.Demographics,
        models.Location,
        models.Travel,
        wimodels.Symptom,
        wimodels.ClinicalFindings,
        models.MicrobiologyTest,
        models.Diagnosis,
        models.Antimicrobial,
        models.MicrobiologyInput,
        wimodels.Management
    ]

class WalkinListGroup(patient_lists.TabbedPatientListGroup):
    member_lists = [
        WalkinNurseTriage,
        WalkinDoctor,
        WalkinReview
    ]
