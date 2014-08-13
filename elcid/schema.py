
from elcid import models
from opal import models as omodels
#from infectioncontrol import models as icmodels

list_columns = [
    models.Demographics,
    models.Location,
    omodels.Tagging,
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
    omodels.Tagging,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.MicrobiologyInput,
    models.GeneralNote,
]

list_columns_infection_control = [
    models.Demographics,
    models.Location,
#    icmodels.ReportedInfection,
    models.MicrobiologyTest,
#    icmodels.InfectionControlAdvice,
]

list_columns_micro = [
    models.Demographics,
    models.Location,
    omodels.Tagging,
    models.Diagnosis,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.MicrobiologyInput,
    models.GeneralNote
]

list_columns_opat = [
    models.Demographics,
    omodels.Tagging,
    models.Location,
    models.Diagnosis,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.Line,
    models.OPATOutstandingIssues,
]

list_columns_opat_review = [
    models.Antimicrobial,
]

list_schemas = {
    'default': list_columns,
    'microbiology': {
        'default': list_columns_micro,
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
    }
}

from obs import models as obsmodels

detail_columns = [
    obsmodels.Observation,
    models.Demographics,
    models.ContactDetails,
    models.Carers,
    models.Location,
    omodels.Tagging,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.Antimicrobial,
    models.Allergies,
    models.MicrobiologyTest,
    models.Line,
    models.OPATLineAssessment,
    models.MicrobiologyInput,
    models.OPATReview,
    models.Travel,
    models.Appointment,
    models.Todo,
    models.OPATOutstandingIssues,
    models.GeneralNote,
 ]

extract_columns = [
    omodels.Tagging,
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.Antimicrobial,
    models.Allergies,
    models.PastMedicalHistory,
    models.MicrobiologyInput,
    models.MicrobiologyTest,
    models.Travel,
    models.Todo,
    models.GeneralNote,
    ]

# Research study schemas

from research import models as researchmodels

list_columns_research_nurse = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.Antimicrobial,
    models.Travel,
    researchmodels.LabSpecimin
    
]

list_columns_scientist = [
    models.Demographics,
    researchmodels.LabSpecimin
]
