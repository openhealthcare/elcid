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
    display_name = 'OPAT Referrals'
    direct_add = False
    tag = "opat"
    subtag = "opat_referrals"
    schema = list_columns_opat
    order = 8


class OPATFollowUp(TaggedPatientList):
    display_name = 'OPAT Follow up'
    direct_add = False
    tag = "opat"
    subtag = "opat_followup"
    schema = list_columns_opat
    order = 9


class OPATCurrent(TaggedPatientList):
    display_name = 'OPAT Current'
    direct_add = False
    tag = "opat"
    subtag = "opat_current"
    schema = list_columns_opat
    order = 10
