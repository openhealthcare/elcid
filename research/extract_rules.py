from research import models
from search.extract_rules import ExtractRule


class LabSpeciminExtractRule(ExtractRule):
    exclude = True
    slug = models.LabSpecimin.get_api_name()


class LabTestExtractRule(ExtractRule):
    exclude = True
    slug = models.LabTest.get_api_name()


class StudyParticipationExtractRule(ExtractRule):
    exclude = True
    slug = models.StudyParticipation.get_api_name()


class RidRTIStudyDiagnosisExtractRule(ExtractRule):
    exclude = True
    slug = models.RidRTIStudyDiagnosis.get_api_name()


class RidRTITestExtractRule(ExtractRule):
    exclude = True
    slug = models.RidRTITest.get_api_name()


class CheckpointsAssayExtractRule(ExtractRule):
    exclude = True
    slug = models.CheckpointsAssay.get_api_name()
