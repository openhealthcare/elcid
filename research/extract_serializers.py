from research import models
from search.extract_serializers import ExtractSerializer


class LabSpeciminSearchRule(ExtractSerializer):
    exclude = True
    slug = models.LabSpecimin.get_api_name()


class LabTestSearchRule(ExtractSerializer):
    exclude = True
    slug = models.LabTest.get_api_name()


class StudyParticipationSearchRule(ExtractSerializer):
    exclude = True
    slug = models.StudyParticipation.get_api_name()


class RidRTIStudyDiagnosisSearchRule(ExtractSerializer):
    exclude = True
    slug = models.RidRTIStudyDiagnosis.get_api_name()


class RidRTITestSearchRule(ExtractSerializer):
    exclude = True
    slug = models.RidRTITest.get_api_name()


class CheckpointsAssaySearchRule(ExtractSerializer):
    exclude = True
    slug = models.CheckpointsAssay.get_api_name()
