"""
[Virtual] Ward Round implementations
"""
import datetime

from opal.models import Episode
from wardround import WardRound

from elcid import models


class HistoricTagsMixin(object):

    @classmethod
    def to_dict(klass, user):
        """
        We're overriding this so that we can set the extra flag on historic Tags.
        """
        return dict(name=klass.name,
                    description=klass.description,
                    episodes=Episode.objects.serialised(user, klass.episodes(),
                                                        episode_history=True,
                                                        historic_tags=True),
                    filters=klass.filters)


class ConsultantReview(WardRound):
    name = "Consultant review"
    description = "Patients diagnosis review"
    filter_template = "wardrounds/consultant_review_filter.html"
    detail_template = 'wardrounds/discharged_detail.html'

    def episodes(self):
        episodes = Episode.objects.exclude(discharge_date=None)
        episodes = episodes.exclude(consultantatdischarge=None)
        episodes = episodes.filter(primarydiagnosis__confirmed=False)

        if self.filter_arg:
            consultant = models.Consultant.objects.get(name=self.filter_arg)
            episodes = episodes.filter(consultantatdischarge__consultant_fk=consultant.id)
        return episodes.order_by("-discharge_date")


class Discharged(HistoricTagsMixin, WardRound):
    name = 'Discharged last week'
    description = 'Patients discharged in the last week'

    filter_template = 'wardrounds/discharged_filter.html'
    detail_template = 'wardrounds/discharged_detail.html'
    filters = {
        'team': 'episode.tagging[0][value]'
    }

    def episodes(self):
        today = datetime.date.today()
        two_weeks_ago = today - datetime.timedelta(days=7)
        episodes = Episode.objects.filter(
            category__in=['inpatient', 'Walkin'],
            discharge_date__gte=two_weeks_ago)
        return episodes


class OPATReviewList(WardRound):
    name = 'OPAT Review'
    description = 'Final review of OPAT patients post end-of-treatment'

    def episodes(self):
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

    def episodes(self):
        return Episode.objects.filter(active=True, tagging__team__name='opat_current')
