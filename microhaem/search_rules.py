from microhaem import models
from search.search_rules import SearchRule


class EpisodeOfNeutropeniaSearchRule(SearchRule):
    exclude = True
    slug = models.EpisodeOfNeutropenia.get_api_name()


class HaemInformationSearchRule(SearchRule):
    exclude = True
    slug = models.HaemInformation.get_api_name()
