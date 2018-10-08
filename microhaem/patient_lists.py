"""
Patient Lists for the Micro service
"""
from opal.core import patient_lists
from elcid import models

list_columns_haem = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.MicrobiologyInput,
]


# class AntimicrobialStewardshipList(patient_lists.TaggedPatientList):
#     display_name = 'Antimicrobial Stewardship'
#     direct_add = True
#     tag = "antimicrobial_stewardship"
#     schema = list_columns_haem
#     order = 16
#     allow_edit_teams = True


# class BacteraemiaReviewList(patient_lists.TaggedPatientList):
#     display_name = 'Bacteraemia Review'
#     direct_add = True
#     tag = "bacteraemia_review"
#     schema = list_columns_haem
#     order = 17
#     allow_edit_teams = True
