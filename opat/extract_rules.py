from opat import models
from search.extract_rules import ExtractRule


class OPATLineAssessmentExtractRule(ExtractRule):
    exclude = True
    slug = models.OPATLineAssessment.get_api_name()


class OPATOutstandingIssuesExtractRule(ExtractRule):
    exclude = True
    slug = models.OPATOutstandingIssues.get_api_name()
