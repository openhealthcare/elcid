"""
Defining the schemas for various list / detail views
"""
from elcid import models
from opat import models as opat_models
from research import models as research_models


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
    opat_models.OPATReview,
    models.Line,
    opat_models.OPATOutstandingIssues,
]

list_columns_opat_review = [
    models.Antimicrobial,
]

from obs import models as obsmodels
from walkin import models as wimodels

list_columns_walkin = [
    models.Demographics,
    models.Location,
    models.Travel,
    wimodels.Symptom,
    wimodels.ClinicalFindings,
    models.MicrobiologyTest,
    models.Diagnosis,
    obsmodels.Observation,
    models.Antimicrobial,
#    wimodels.Management,
    models.MicrobiologyInput
]

list_columns_walkin_review = [
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

list_columns_triage = [
    models.Demographics,
    models.Location,
    models.Travel,
    wimodels.Symptom,
    models.MicrobiologyTest,
    obsmodels.Observation,
]

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
    'walkin': {
        'walkin_triage': list_columns_triage,
        'walkin_review': list_columns_walkin_review,
        'default': list_columns_walkin
    }
}

# Research study schemas

from research import models as researchmodels

list_columns_research_practitioner = [
    models.Demographics,
    models.Location,
    research_models.RidRTIStudyDiagnosis,
    models.Diagnosis,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.Travel,
    research_models.LabTest,
    research_models.LabSpecimin
]

list_columns_scientist = [
    models.Demographics,
    research_models.RidRTIStudyDiagnosis,
    research_models.LabTest,
    research_models.CheckpointsAssay,
    research_models.RidRTITest
]
