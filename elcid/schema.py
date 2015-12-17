"""
Defining the schemas for various list / detail views
"""
from elcid import models
from research import models as research_models
from infectiousdiseases import schema as id_schema

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

list_columns_infection_control = [
    models.Demographics,
    models.Location,
    models.MicrobiologyTest,
]


list_schemas = {
    'default': list_columns,
    'microbiology': {
        'default': id_schema.list_columns_micro,
        },
    'virology': {
        'default': id_schema.list_columns_micro
    },
    'infectioncontrol': {
        'default': list_columns_infection_control
    },
    'infectious_diseases': {
        # 'default': list_columns,
        'id_liaison': id_schema.list_columns_id_liaison
    },
}


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
