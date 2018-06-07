from opat import models
from search.search_rules import SearchRule


class OPATLineAssessmentearchRule(SearchRule):
    exclude = True
    slug = models.OPATLineAssessment.get_api_name()


class OPATOutstandingIssuesSearchRule(SearchRule):
    exclude = True
    slug = models.OPATOutstandingIssues.get_api_name()
