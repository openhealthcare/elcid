from opal.core.patient_lists import TaggedPatientList
from opat import models as opat_models
from elcid import models

list_columns_opat = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.Antimicrobial,
    models.MicrobiologyTest,
    opat_models.OPATReview,
    models.Line,
    opat_models.OPATOutstandingIssues,
]


class OPATReferral(TaggedPatientList):
    tag = "opat"
    subtag = "opat_referrals"
    schema = list_columns_opat


class OPATFollowUp(TaggedPatientList):
    tag = "opat"
    subtag = "opat_followup"
    schema = list_columns_opat


class OPATCurrent(TaggedPatientList):
    tag = "opat"
    subtag = "opat_current"
    schema = list_columns_opat
