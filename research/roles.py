"""
Research study roles ! 
"""
import collections

def get_study_roles(user):
    """
    Given a USER, return a set of roles that this user fills for our
    active research studies.
    """
    # This has to be here because Django wants to make sure it's the first
    # thing to import models and gets distinctly snippish if you beat it.
    from research.models import ResearchStudy
    
    roles = collections.defaultdict(list)

    for study in user.clinical_lead_user.all():
        roles[study.team_name].append('clinical_lead')

    for study in user.researcher_user.all():
        roles[study.team_name].append('researcher')

    for study in user.research_nurse_user.all():
        roles[study.team_name].append('research_practitioner')

    for study in user.scientist_user.all():
        roles[study.team_name].append('scientist')
        
    return roles
