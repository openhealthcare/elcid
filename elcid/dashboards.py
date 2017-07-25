"""
elCID Dashboards
"""
import datetime

from django.utils.functional import cached_property
from django.core.urlresolvers import reverse

from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlencode


from dashboard import Dashboard, widgets
from django.db.models import Count
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
        dates = Episode.objects.filter(start__gte=twentyten).values('start').annotate(Count('start'))
        ticks = ['x']
        lines = ['Start']
        for date in dates:
            if date['start']:
                ticks.append(date['start'].isoformat())
                lines.append(date['start__count'])

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
            episodes = Episode.objects.exclude(end=None)
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
