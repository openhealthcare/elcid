"""
Patient Lists for the OPAT service
"""
from opal.core import patient_lists
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


class OPATReferral(patient_lists.TaggedPatientList):
    display_name = 'OPAT Referrals'
    direct_add = False
    tag = "opat"
    subtag = "opat_referrals"
    schema = list_columns_opat
    order = 8
    allow_edit_teams = False


class OPATFollowUp(patient_lists.TaggedPatientList):
    display_name = 'OPAT Follow up'
    direct_add = False
    tag = "opat"
    subtag = "opat_followup"
    schema = list_columns_opat
    order = 10
    allow_edit_teams = False


class OPATCurrent(patient_lists.TaggedPatientList):
    display_name = 'OPAT Current'
    direct_add = False
    tag = "opat"
    subtag = "opat_current"
    schema = list_columns_opat
    order = 9
    allow_edit_teams = False


class OPATListGroup(patient_lists.TabbedPatientListGroup):
    member_lists = [
        OPATReferral,
        OPATCurrent,
        OPATFollowUp,
    ]
    display_name = "OPAT"
