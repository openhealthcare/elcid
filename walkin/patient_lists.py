from elcid import models
from obs import models as obsmodels
from walkin import models as wimodels
from opal.core.patient_lists import PatientList, TaggedPatientList


class WalkinDoctor(TaggedPatientList, PatientList):
    tag = "walkin"
    subtag = "walkin_doctor"
    schema = [
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


class WalkinNurseTriage(TaggedPatientList, PatientList):
    tag = "walkin"
    subtag = "walkin_triage"
    schema = [
        models.Demographics,
        models.Location,
        models.Travel,
        wimodels.Symptom,
        models.MicrobiologyTest,
        obsmodels.Observation,
    ]


class WalkinReview(TaggedPatientList, PatientList):
    tag = "walkin"
    subtag = "walkin_review"
    schema = [
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
