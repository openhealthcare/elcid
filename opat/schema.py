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

list_columns_opat_review = [
    models.Antimicrobial,
]
