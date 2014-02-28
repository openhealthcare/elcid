
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

detail_columns = [
    models.Demographics,
    models.Location,
    models.Allergies,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.MicrobiologyInput,
    models.MicrobiologyTest,
    models.Antimicrobial,
    models.Travel,
    models.Todo,
    models.GeneralNote,
]

extract_columns = [
    omodels.Tagging,
    models.Demographics,
    models.Location,
    models.Allergies,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.MicrobiologyInput,
    models.MicrobiologyTest,
    models.Antimicrobial,
    models.Travel,
    models.Todo,
    models.GeneralNote,
    ]
