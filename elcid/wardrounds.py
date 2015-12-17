"""
[Virtual] Ward Round implementations
"""
import datetime

from opal.models import Episode
from wardround import WardRound


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


class Discharged(HistoricTagsMixin, WardRound):
    name = 'Discharged last week'
    description = 'Patients discharged in the last week'

    filter_template = 'wardrounds/discharged_filter.html'
    detail_template = 'wardrounds/discharged_detail.html'
    filters = {
        'team': 'episode.tagging[0][value]'
    }

    @staticmethod
    def episodes():
        today = datetime.date.today()
        two_weeks_ago = today - datetime.timedelta(days=7)
        episodes = Episode.objects.filter(
            category__in=['inpatient', 'Walkin'],
            discharge_date__gte=two_weeks_ago)
        return episodes
