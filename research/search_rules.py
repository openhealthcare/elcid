from research import models
from search.search_rules import SearchRule


class LabSpeciminSearchRule(SearchRule):
    exclude = True
    slug = models.LabSpecimin.get_api_name()


class LabTestSearchRule(SearchRule):
    exclude = True
    slug = models.LabTest.get_api_name()


class StudyParticipationSearchRule(SearchRule):
    exclude = True
    slug = models.StudyParticipation.get_api_name()


class RidRTIStudyDiagnosisSearchRule(SearchRule):
    exclude = True
    slug = models.RidRTIStudyDiagnosis.get_api_name()


class RidRTITestSearchRule(SearchRule):
    exclude = True
    slug = models.RidRTITest.get_api_name()


class CheckpointsAssaySearchRule(SearchRule):
    exclude = True
    slug = models.CheckpointsAssay.get_api_name()
