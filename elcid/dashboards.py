"""
elCID Dashboards
"""
import collections 

from dashboard import Dashboard, widgets
from django.db.models import Count
from opal.models import Episode

from elcid.models import Diagnosis

class NumberOfDiagnoses(widgets.Number):
    tagline = 'Diagnoses made'
    
    @classmethod
    def get_number(kls):
        return Diagnosis.objects.count()

class CurrentPatients(widgets.Number):
    tagline = 'Active'

    @classmethod
    def get_number(kls):
        return Episode.objects.filter(active=True).count()

class Admissions(widgets.LineChart):
    tagline = 'Admissions'
    slug = 'elcid-admissions'

    @classmethod
    def get_lines(kls):
        dates = Episode.objects.values('date_of_admission').annotate(Count('date_of_admission'))
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

    @classmethod
    def get_widgets(user):
        return [
            Admissions,
            widgets.NumberOfUsers,
            widgets.NumberOfEpisodes,
            NumberOfDiagnoses,
            CurrentPatients,
        ]
