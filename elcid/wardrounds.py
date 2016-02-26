"""
[Virtual] Ward Round implementations
"""
from datetime import timedelta, date

from opal.models import Episode, Tagging
from wardround.wardrounds import WardRound
from elcid.models import Consultant, OPATMeta


class HistoricTagsMixin(object):
    def to_dict(self):
        """
        We're overriding this so that we can set the extra flag on historic Tags.
        """
        return dict(name=self.name,
                    description=self.description,
                    episodes=Episode.objects.serialised(
                        self.request.user,
                        self.episodes(),
                        episode_history=True,
                        historic_tags=True),
                    )


class Discharged(HistoricTagsMixin, WardRound):
    name = 'Discharged last week'
    description = 'Patients discharged in the last week'

    filter_template = 'wardrounds/discharged_filter.html'
    detail_template = 'wardrounds/discharged_detail.html'
    filters = {
        'team': 'episode.tagging[0][value]'
    }

    def episodes(self):
        today = date.today()
        two_weeks_ago = today - timedelta(days=7)
        team = self.request.GET.get("team", None)

        episodes = Episode.objects.filter(
            category__in=['inpatient', 'Walkin'],
            discharge_date__gte=two_weeks_ago)
        if team:
            return episodes.filter(tagging__team__name=team)
        else:
            return episodes


class ConsultantReview(WardRound):
    name = "Consultant review"
    description = "Patients diagnosis review"
    filter_template = "wardrounds/consultant_review_filter.html"
    detail_template = 'wardrounds/discharged_detail.html'

    def episodes(self):
        consultant_name = self.request.GET.get("consultant_at_discharge", None)

        episodes = Episode.objects.exclude(discharge_date=None)
        episodes = episodes.exclude(consultantatdischarge__consultant_fk=None)
        episodes = episodes.filter(primarydiagnosis__confirmed=False)

        if consultant_name:
            consultant = Consultant.objects.get(name=consultant_name)
            episodes = episodes.filter(
                consultantatdischarge__consultant_fk=consultant.id
            )

        return episodes.order_by("-discharge_date")


class OPATReviewList(WardRound):
    name = 'OPAT Review'
    description = 'Final review of OPAT patients post end-of-treatment'

    def episodes(self):
        review_ready = OPATMeta.objects.filter(review_date__lte=date.today())
        in_round = set()
        for om in review_ready:
            if om.episode.opatoutcome_set.filter(outcome_stage='OPAT Review').count() == 0:
                in_round.add(om.episode.id)
        return Episode.objects.filter(id__in=in_round)

    detail_template = 'wardrounds/opat_detail.html'


class OPATCurrentList(WardRound):
    name        = 'OPAT Current'
    description = 'All patients on the OPAT current list'

    def episodes(self):
        return Episode.objects.filter(
            active=True,
            tagging__team__name='opat_current',
            tagging__archived=False
        )
