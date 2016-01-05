from elcid import models
from research import models as research_models
from opal.core.patient_lists import TaggedPatientList


class RidRtiScientist(TaggedPatientList):
    tag = "rid_rti"
    subtag = "rid_rti_scientist"
    schema = [
        models.Demographics,
        research_models.RidRTIStudyDiagnosis,
        research_models.LabTest,
        research_models.CheckpointsAssay,
        research_models.RidRTITest
    ]


class RidRtiResearchPractitioner(TaggedPatientList):
    tag = "rid_rti"
    subtag = "rid_rti_research_practitioner"
    schema = [
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
