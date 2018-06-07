from walkin import models
from search.search_rules import SearchRule


class ZikaPathwayExtractRule(SearchRule):
    exclude = True
    slug = models.ZikaPathway.get_api_name()
