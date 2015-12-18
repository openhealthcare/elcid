from elcid import models
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
