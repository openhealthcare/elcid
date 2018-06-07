from walkin import models
from search.extract_rules import ExtractRule


class ZikaPathwayExtractRule(ExtractRule):
    exclude = True
    slug = models.ZikaPathway.get_api_name()
