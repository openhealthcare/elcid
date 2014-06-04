
from elcid import models
from opal import models as omodels

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
list_columns_infection_control = [
    models.Demographics,
    models.Location,
    models.MicrobiologyTest,
]
list_columns_micro = [
    models.Demographics,
    models.Location,
    omodels.Tagging,
    models.Diagnosis,
    models.Antimicrobial,
    models.MicrobiologyTest,
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
    models.OPATOutstandingIssues
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
            'default': list_columns_infection_control}
}

detail_columns = [
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
    models.MicrobiologyInput,
    models.OPATReview,
    models.Travel,
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
