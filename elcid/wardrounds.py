"""
[Virtual] Ward Round implementations
"""
import datetime

from opal.models import Episode
from wardround.wardrounds import WardRound


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
    display_name = 'Discharged last week'
    description = 'Patients discharged in the last week'

    filter_template = 'wardrounds/discharged_filter.html'
    detail_template = 'wardrounds/discharged_detail.html'
    filters = {
        'team': 'episode.tagging[0][value]'
    }

    def episodes(self):
        today = datetime.date.today()
        two_weeks_ago = today - datetime.timedelta(days=7)
        team = self.request.GET.get("team", None)

        episodes = Episode.objects.filter(
            category__in=['Inpatient', 'Walkin'],
            discharge_date__gte=two_weeks_ago)

        if team:
            episodes = episodes.filter(tagging__value=team)

        return episodes
