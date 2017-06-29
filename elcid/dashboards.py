"""
elCID Dashboards
"""
import datetime
from django.db.models import Count, Min, F, Max, Avg

from django.utils.functional import cached_property
from django.core.urlresolvers import reverse
from urllib import urlencode
from opal.core.subrecords import episode_subrecords


from dashboard import Dashboard, widgets
from opal.models import Episode
from elcid.models import Diagnosis, Consultant


class NumberOfDiagnoses(widgets.Number):
    tagline = 'Diagnoses made'

    def get_number(self):
        return Diagnosis.objects.count()


class CurrentPatients(widgets.Number):
    tagline = 'Active'

    def get_number(self):
        return Episode.objects.filter(active=True).count()


class Admissions(widgets.LineChart):
    tagline = 'Admissions'
    slug = 'elcid-admissions'

    def get_lines(self):
        twentyten = datetime.datetime(2013, 1, 1)
        dates = Episode.objects.filter(date_of_admission__gte=twentyten).values('date_of_admission').annotate(Count('date_of_admission'))
        ticks = ['x']
        lines = ['Date of admission']
        for date in dates:
            if date['date_of_admission']:
                ticks.append(date['date_of_admission'].isoformat())
                lines.append(date['date_of_admission__count'])

        return [ticks, lines]


class ConfirmedDiagnosisByConsultant(widgets.Table):

    tagline = "Confirmed Diagnosis by Consultant"
    TOTAL_NUMBER = "Total Number of Patients"
    CONFIRMED_DIAGNOSIS = "% Confirmed Diagnosis"
    CONSULTANT = "Consultant"
    table_headers = [CONSULTANT, TOTAL_NUMBER, CONFIRMED_DIAGNOSIS]
    include_index=True

    @cached_property
    def table_data(self):
        rows = []
        consultants = Consultant.objects.all()

        for consultant in consultants:
            row = {}
            row[self.CONSULTANT] = consultant.name
            link = reverse("wardround_index")
            link_args = urlencode({"consultant_at_discharge": consultant.name})
            link = link + "#/consultantreview?" + link_args
            consultant_link = "%s__link" % self.CONSULTANT
            row[consultant_link] = link
            episodes = Episode.objects.exclude(discharge_date=None)
            episodes = episodes.filter(consultantatdischarge__consultant_fk=consultant.pk)
            row[self.TOTAL_NUMBER] = episodes.count()
            with_confirmed = episodes.filter(primarydiagnosis__confirmed=True)
            confirmed_diagnosis = with_confirmed.distinct().count()

            if row[self.TOTAL_NUMBER] > 0:
                completed = float(confirmed_diagnosis)/float(row[self.TOTAL_NUMBER])
                row[self.CONFIRMED_DIAGNOSIS] = int(100 * completed)

            if row.get(self.CONFIRMED_DIAGNOSIS, 51) < 50:
                row[self.row_class] = "diagnosis-table-issue"
            rows.append(row)

        rows = sorted(rows, key=lambda x: x[self.CONSULTANT])
        rows = sorted(rows, key=lambda x: x.get(self.CONFIRMED_DIAGNOSIS, 101))

        for i, row in enumerate(rows, start=1):
            if row[self.TOTAL_NUMBER] == 0:
                row['number'] = '-'
            else:
                row['number'] = i
        return rows


class UsageDashboard(Dashboard):
    """
    Dashboard relaying core usage statistics for elCID
    """
    display_name        = 'elCID Metrics'
    description = 'Core metrics for the elCID service.'

    def get_widgets(user):
        return [
            Admissions,
            widgets.NumberOfUsers,
            widgets.NumberOfEpisodes,
            NumberOfDiagnoses,
            CurrentPatients,
        ]


class SubrecordTrends(widgets.Table):
    """
        This Dashboard
        Assuming that the first subrecord is created when the
        episode is created
        1. The average time a subrecord has been created after the episode is created
        2. The average amount of a subrecord that is created
    """
    tagline = "User trends"
    SUBRECORD_NAME = "Subrecord"
    # AVG_SPEED_CREATED = "avg_created"
    AVG_COUNT_PER_EPISODE = "avg_count"
    MIN_COUNT_PER_EPISODE = "min_count"
    MAX_COUNT_PER_EPISODE = "max_count"
    table_headers = [
        SUBRECORD_NAME,
        # AVG_SPEED_CREATED,
        MIN_COUNT_PER_EPISODE,
        AVG_COUNT_PER_EPISODE,
        MAX_COUNT_PER_EPISODE
    ]

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
                "{}_diff_created".format(related_name): f_base - F(min_created)
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
                # max_diff=Max(field),
                # min_diff=Min(field),
                # avg_created=Min(field),
                max_count=Max(count_field),
                avg_count=Avg(count_field),
                min_count=Min(count_field)
            )
            row[self.SUBRECORD_NAME] = display_name
            result.append(row)
        return result

    def all_episodes(self):
        qs = Episode.objects.all()
        qs = self.get_min_episode(qs)
        qs = self.get_min(qs)
        qs = self.get_subrecord_difference(qs, F('min_created'))
        return self.subrecord_detail(qs)

    @cached_property
    def table_data(self):
        return self.all_episodes()


class TrendsDashboard(Dashboard):
    """
    Dashboard relaying core usage statistics for elCID
    """
    display_name = 'elCID Trends'
    description = 'Trends in the way users use the elCID service.'

    def get_widgets(user):
        return [
            SubrecordTrends,
        ]
