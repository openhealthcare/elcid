"""
elCID Dashboards
"""
import datetime

from dashboard import Dashboard, widgets
from django.db.models import Count
from opal.models import Episode
from elcid.models import Diagnosis


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


class UsageDashboard(Dashboard):
    """
    Dashboard relaying core usage statistics for elCID
    """
    name        = 'elCID Metrics'
    description = 'Core metrics for the elCID service.'

    def get_widgets(user):
        return [
            Admissions,
            widgets.NumberOfUsers,
            widgets.NumberOfEpisodes,
            NumberOfDiagnoses,
            CurrentPatients,
        ]
