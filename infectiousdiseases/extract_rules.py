from search import extract_rules
from infectiousdiseases import models


class ExternalLiaisonContactDetailsSearchRule(extract_rules.ExtractRule):
    exclude = True
    slug = models.ExternalLiaisonContactDetails.get_api_name()
    model = models.ExternalLiaisonContactDetails
