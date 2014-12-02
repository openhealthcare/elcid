"""
[Virtual] Ward Round implementations
"""
from opal.models import Episode
from wardround import WardRound

from elcid.models import PrimaryDiagnosis

class MicroHaem(WardRound):
    name        = 'Micro Haem'
    description = 'All patients on the Micro haem list in ward location order'

    @staticmethod
    def episodes():
        return Episode.objects.filter(active=True, tagging__team__name='micro_haem')


class FinalDiagnosisReview(WardRound):
    name        = 'Final Diagnosis Review'
    description = 'Discharged Patients with a final diagnosis for consultant review.'
    
    filter_template = 'wardrounds/final_diagnosis_filter.html'
    filters    = {
        'discharge_from': 'episode.discharge_date >= moment(value, "DD-MM-YYYY")',
        'discharge_to'  : 'episode.discharge_date <= moment(value, "DD-MM-YYYY")'
    }
    
    @staticmethod
    def episodes():
        unconfirmed = PrimaryDiagnosis.objects.filter(confirmed=False)
        return set([d.episode for d in unconfirmed])
