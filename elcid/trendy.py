from opal import models
from opal.core.subrecords import episode_subrecords
from django.db.models import Count, Min, F, Max, Avg


class SubrecordTrends(object):
    def __init__(self, request_get_args):
        team = request_get_args.pop("team")
        qs = models.Episode.objects.all()
        qs = qs.filter(tagging__value=team)
        qs = self.get_min_episode(qs)
        qs = self.get_min(qs)
        qs = self.get_subrecord_difference(qs, F('min_created'))
        return self.subrecord_detail(qs)

    def get_min_episode(self, qs):
        # annotates an episode queryset with extra fields
        # of the min created for non singleton subrecords
        # and min updated for singleton subrecord
        qs = qs.select_related()

        for subrecord in episode_subrecords():
            related_name = subrecord.__name__.lower()
            if subrecord._is_singleton:
                # if its a singleton, created is never populated, updated is
                # so use this as created
                min_updated = {
                    "{0}_min_created".format(related_name): Min(
                        "{}__updated".format(related_name)
                    )
                }
                qs = qs.annotate(
                    **min_updated
                )
            else:
                min_created = {
                    "{0}_min_created".format(related_name): Min(
                        "{}__created".format(related_name)
                    )
                }
                qs = qs.annotate(
                    **min_created
                )
            total_count = {
                "{0}_count".format(related_name): Count(
                    related_name
                )
            }
            qs = qs.annotate(**total_count)

        return qs

    def get_min(self, qs):
        # get's the min of all the subrecord mins
        min_args = []
        for subrecord in episode_subrecords():
            related_name = subrecord.__name__.lower()
            min_args.append(F("{0}_min_created".format(related_name)))
        return qs.annotate(min_created=min(*min_args))

    def get_subrecord_difference(self, qs, f_base):
        # for each subrecord, give me the difference between
        # some f expression and when it was created or updated
        for Subrecord in episode_subrecords():
            related_name = Subrecord.__name__.lower()
            min_created = "{0}_min_created".format(related_name)
            qs = qs.annotate(**{
                "{}_diff_created".format(related_name): F(min_created) - f_base
            })
        return qs

    def subrecord_detail(self, qs):
        result = []
        for Subrecord in episode_subrecords():
            related_name = Subrecord.__name__.lower()
            display_name = Subrecord.get_display_name()
            field = "{0}_diff_created".format(related_name)
            count_field = "{0}_count".format(related_name)
            row = qs.aggregate(
                avg_created=Min(field),
                max_count=Max(count_field),
                avg_count=Avg(count_field),
                min_count=Min(count_field)
            )
            row[self.SUBRECORD_NAME] = display_name
            row[self.SUBRECORD_DETAIL] = self.get_aggregate_subrecord_summary(
                Subrecord, qs
            )
            result.append(row)
        return result

    def all_episodes(self):
        qs = models.Episode.objects.all()
        qs = self.get_min_episode(qs)
        qs = self.get_min(qs)
        qs = self.get_subrecord_difference(qs, F('min_created'))
        return self.subrecord_detail(qs)
