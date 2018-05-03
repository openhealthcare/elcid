from research import models
from search.extract_rules import ExtractRule


class LabSpeciminSearchRule(ExtractRule):
    exclude = True
    slug = models.LabSpecimin.get_api_name()


class LabTestSearchRule(ExtractRule):
    exclude = True
    slug = models.LabTest.get_api_name()


class StudyParticipationSearchRule(ExtractRule):
    exclude = True
    slug = models.StudyParticipation.get_api_name()


class RidRTIStudyDiagnosisSearchRule(ExtractRule):
    exclude = True
    slug = models.RidRTIStudyDiagnosis.get_api_name()


class RidRTITestSearchRule(ExtractRule):
    exclude = True
    slug = models.RidRTITest.get_api_name()


class CheckpointsAssaySearchRule(ExtractRule):
    exclude = True
    slug = models.CheckpointsAssay.get_api_name()
