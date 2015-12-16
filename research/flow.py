"""
Fetch flows for our active studies! 
"""
import collections

def get_study_flows():
    """
    Return a dict of flows to be used with our research studies.
    """
    # This has to be here because Django wants to make sure it's the first
    # thing to import models and gets distinctly snippish if you beat it.
    from research.models import ResearchStudy

    flows = collections.defaultdict(dict)
    for study in ResearchStudy.objects.filter(active=True):
        flows[study.team_name]['default'] = {
            'enter': {
                'controller': 'ResearchStudyHospitalNumberCtrl',
                'template'  : '/templates/modals/hospital_number.html'
            },
            'exit': {
                'controller': 'ResearchStudyDischargeCtrl',
                'template'  : '/research/templates/discharge.html' 
            }
        }
    return flows 
