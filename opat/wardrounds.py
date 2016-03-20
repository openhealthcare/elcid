from wardround.wardrounds import WardRound
from datetime import datetime, date
from opat import models
from opal.models import Episode


class OPATReviewList(WardRound):
    display_name = 'OPAT Review'
    description  = 'Final review of OPAT patients post end-of-treatment'

    def episodes(self):
        review_ready = models.OPATMeta.objects.filter(review_date__lte=date.today())
        in_round = set()
        for om in review_ready:
            if om.episode.opatoutcome_set.filter(outcome_stage='OPAT Review').count() == 0:
                in_round.add(om.episode.id)
        return Episode.objects.filter(id__in=in_round)

    detail_template = 'wardrounds/opat_detail.html'


class OPATCurrentList(WardRound):
    display_name = 'OPAT Current'
    description  = 'All patients on the OPAT current list'

    def episodes(self):
        return Episode.objects.filter(active=True,
                                      tagging__team__name='opat_current',
                                      tagging__archived=False)
