"""
[Virtual] Ward Round implementations
"""
from opal.models import Episode

from wardround import WardRound

class MicroHaem(WardRound):
    name        = 'Micro Haem'
    description = 'All patients on the Micro haem list in ward location order'

    @staticmethod
    def episodes():
        return Episode.objects.filter(active=True, tagging__team__name='micro_haem')


class FinalDiagnosisReview(WardRound):
    name        = 'Final Diagnosis Review'
    description = 'Discharged Patients with a final diagnosis for consultant review.'

    @staticmethod
    def episodes():
        return Episode.objects.filter(active=True)
