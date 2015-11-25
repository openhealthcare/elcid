"""
Defining the schemas for various list / detail views
"""
from elcid import models
from opal import models as omodels

list_columns = [
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

list_columns_id_liaison = [
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

list_columns_infection_control = [
    models.Demographics,
    models.Location,
    models.MicrobiologyTest,
]

list_columns_micro = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.MicrobiologyInput,
    models.GeneralNote
]

list_columns_opat = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.OPATReview,
    models.Line,
    models.OPATOutstandingIssues,
]

list_columns_opat_review = [
    models.Antimicrobial,
]

# from obs import models as obsmodels
#
# list_columns_triage = [
#     models.Demographics,
#     models.Location,
#     models.Travel,
#     wimodels.Symptom,
#     models.MicrobiologyTest,
#     obsmodels.Observation,
# ]

list_schemas = {
    'default': list_columns,
    'microbiology': {
        'default': list_columns_micro,
        },
    'virology': {
        'default': list_columns_micro
    },
    'opat': {
        'default': list_columns_opat,
#        'opat_review': list_columns_opat_review
        },
    'infectioncontrol': {
        'default': list_columns_infection_control
    },
    'infectious_diseases': {
        # 'default': list_columns,
        'id_liaison': list_columns_id_liaison
    },
}

# Research study schemas
#
# from research import models as researchmodels
#
# list_columns_research_practitioner = [
#     models.Demographics,
#     models.Location,
#     models.RidRTIStudyDiagnosis,
#     models.Diagnosis,
#     models.Antimicrobial,
#     models.MicrobiologyTest,
#     models.LabTest,
#     models.Travel,
#     models.LabSpecimin
# ]
#
# list_columns_scientist = [
#     models.Demographics,
#     models.RidRTIStudyDiagnosis,
#     models.LabTest,
#     models.CheckpointsAssay,
#     models.RidRTITest
# ]
