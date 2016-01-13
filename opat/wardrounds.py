from wardround import WardRound
from datetime import datetime
from opat import models
from opal.models import Episode

class OPATReviewList(WardRound):
    name = 'OPAT Review'
    description = 'Final review of OPAT patients post end-of-treatment'

    @staticmethod
    def episodes():
        review_ready = models.OPATMeta.objects.filter(review_date__lte=datetime.date.today())
        in_round = set()
        for om in review_ready:
            if om.episode.opatoutcome_set.filter(outcome_stage='OPAT Review').count() == 0:
                in_round.add(om.episode)
        return in_round

    detail_template = 'wardrounds/opat_detail.html'


class OPATCurrentList(WardRound):
    name        = 'OPAT Current'
    description = 'All patients on the OPAT current list'

    @staticmethod
    def episodes():
        return Episode.objects.filter(active=True, tagging__team__name='opat_current')
