from elcid import models
from obs import models as obsmodels
from walkin import models as wimodels
from opal.core.patient_lists import TaggedPatientList


class WalkinDoctor(TaggedPatientList):
    display_name = 'Walkin Doctor'
    direct_add = True
    tag = "walkin"
    subtag = "walkin_doctor"
    order = 12
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


class WalkinNurseTriage(TaggedPatientList):
    display_name = 'Walkin Nurse Triage'
    direct_add = True
    tag = "walkin"
    subtag = "walkin_triage"
    order = 11
    schema = [
        models.Demographics,
        models.Location,
        models.Travel,
        wimodels.Symptom,
        models.MicrobiologyTest,
        obsmodels.Observation,
    ]


class WalkinReview(TaggedPatientList):
    display_name = 'Walkin Review'
    direct_add = True
    tag = "walkin"
    subtag = "walkin_review"
    order = 13
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
