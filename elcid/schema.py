
from elcid import models
from opal import models as omodels

list_columns = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.AntimicrobialPlan,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.Line,
    models.OPATOutstandingIssues,
    # models.PastMedicalHistory,
    # models.Travel,
    # models.GeneralNote,
    # models.Todo,
]

detail_columns = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.AntimicrobialPlan,
    models.Antimicrobial,
    models.Allergies,
    models.MicrobiologyTest,
    models.Line,
    models.OPATReview,
    models.OPATOutstandingIssues,
    # models.MicrobiologyInput,
    # models.Travel,
    # models.Todo,
    # models.GeneralNote,
]

extract_columns = [
    omodels.Tagging,
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.Antimicrobial,
    # models.Allergies,
    # models.PastMedicalHistory,
    # models.MicrobiologyInput,
    # models.MicrobiologyTest,
    # models.Travel,
    # models.Todo,
    # models.GeneralNote,
    ]
