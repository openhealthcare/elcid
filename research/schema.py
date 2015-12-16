"""
Create/fetch schemas for our studies.
"""
import collections

from django.conf import settings

from opal.utils import stringport

def get_study_schemas():
    """
    Return a dict of schemas to be used with our research studies.
    """
    # This has to be here because Django wants to make sure it's the first
    # thing to import models and gets distinctly snippish if you beat it.
    from research.models import ResearchStudy

    research_nurse_schema = stringport(settings.LIST_SCHEMA_RESEARCH_PRACTITIONER)
    scientist_schema = stringport(settings.LIST_SCHEMA_SCIENTIST)

    schemas = collections.defaultdict(dict)
    for study in ResearchStudy.objects.filter(active=True):
        schemas[study.team_name][study.team_name + '_research_practitioner'] = research_nurse_schema
        schemas[study.team_name][study.team_name + '_scientist'] = scientist_schema
    return schemas
