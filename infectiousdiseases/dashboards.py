from urllib import urlencode

from dashboard import Dashboard, widgets
from django.core.urlresolvers import reverse
from opal.models import Episode
from django.utils.functional import cached_property
from elcid.models import Consultant


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
            if row[self.TOTAL_NUMBER] == 0:
                row[self.CONFIRMED_DIAGNOSIS] = 100
            else:
                completed = float(confirmed_diagnosis)/float(row[self.TOTAL_NUMBER])
                row[self.CONFIRMED_DIAGNOSIS] = int(100 * completed)

            if row[self.CONFIRMED_DIAGNOSIS] < 50:
                row[self.row_class] = "diagnosis-table-issue"

            rows.append(row)

        rows = sorted(rows, key=lambda x: x[self.CONSULTANT])
        return sorted(rows, key=lambda x: x[self.CONFIRMED_DIAGNOSIS])


class ConfirmedDiagnosis(Dashboard):
    """
    Dashboard relaying stats about the number of patients discharged
    by named consultants
    """
    display_name = "Consultant Review Dashboard"
    description = "Statistics about the number of discharged patients with confirmed diagnoses"

    def get_widgets(user):
        return [ConfirmedDiagnosisByConsultant]
