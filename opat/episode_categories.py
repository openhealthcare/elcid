from opal.core import episodes
from django.utils.functional import cached_property


class OPATEpisode(episodes.EpisodeCategory):
    display_name            = 'OPAT'
    detail_template = 'detail/opat2.html'

    @cached_property
    def tags(self):
        return self.episode.get_tag_names(None)

    @cached_property
    def rejection_date(self):
        rejection = self.episode.opatrejection_set.first()
        if rejection:
            return rejection.date

    @property
    def start(self):
        if self.rejection_date:
            return self.rejection_date

        if "opat_referrals" in self.tags:
            return None

        return self.episode.location_set.first().opat_acceptance

    @property
    def end(self):
        if self.rejection_date:
            return self.rejection_date

        if "opat_referrals" in self.tags:
            return None

        return super(OPATEpisode, self).end
