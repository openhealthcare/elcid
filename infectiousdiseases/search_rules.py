from infectiousdiseases import models
from search.search_rules import SearchRule


class ExternalLiaisonContactDetailsSearchRule(SearchRule):
    exclude = True
    display_name = "Liason Contact Details"
    slug = models.ExternalLiaisonContactDetails.get_api_name()
    model = models.ExternalLiaisonContactDetails
