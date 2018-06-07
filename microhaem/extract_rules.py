from microhaem import models
from search.extract_rules import ExtractRule


class EpisodeOfNeutropeniaExtractRule(ExtractRule):
    exclude = True
    slug = models.EpisodeOfNeutropenia.get_api_name()


class HaemInformationExtractRule(ExtractRule):
    exclude = True
    slug = models.HaemInformation.get_api_name()
