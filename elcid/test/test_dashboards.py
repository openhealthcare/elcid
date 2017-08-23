from datetime import date, timedelta

from django.core.urlresolvers import reverse

from opal.core.test import OpalTestCase
from opal.models import Patient
from elcid.models import Consultant
from elcid.dashboards import ConfirmedDiagnosisByConsultant


class ConfirmedDiagnosisTestCase(OpalTestCase):
    def create_test_episode(
        self, consultant=None, end=None, confirmed_diagnosis=False
    ):
        patient = Patient.objects.create()
        consultant, _ = Consultant.objects.get_or_create(name=consultant)
        kwargs = {}

        if end:
            kwargs = {"end": end}

        episode = patient.create_episode(**kwargs)

        if consultant is not None:
            discharge_consultant = episode.consultantatdischarge_set.first()
            discharge_consultant.consultant = consultant.name
            discharge_consultant.save()

        if confirmed_diagnosis:
            primary_diagnosis = episode.primarydiagnosis_set.first()
            primary_diagnosis.confirmed = confirmed_diagnosis
            primary_diagnosis.save()

        return episode

    def test_get(self):
        yesterday = date.today() - timedelta(1)
        url = reverse("dashboard_detail", kwargs=dict(name="consultant_review_dashboard"))
        self.create_test_episode(
            consultant="Jane", end=yesterday
        )
        self.client.login(username=self.user.username, password=self.PASSWORD)
        response = self.client.get(url)
        self.assertContains(response, "Jane")

    def test_data_dict(self):
        # cases we need to test
        # make sure we don't get a divide by 0 error if there are no episodes
        # make sure we only count future episodes
        # make sure ordering is correct

        yesterday = date.today() - timedelta(1)

        self.create_test_episode(
            consultant="Jane", end=yesterday
        )

        self.create_test_episode(
            consultant="Jane", end=yesterday, confirmed_diagnosis=True
        )

        self.create_test_episode(
            consultant="Jane"
        )

        self.create_test_episode(
            consultant="Ben", end=yesterday, confirmed_diagnosis=True
        )

        Consultant.objects.create(name="No Episodes")
        widget = ConfirmedDiagnosisByConsultant()
        result = widget.table_data

        expected = [
            {
                'number': 1,
                '% Confirmed Diagnosis': 50,
                'Consultant': u'Jane',
                'Total Number of Patients': 2,
                'Consultant__link': u'/wardround/#/consultantreview?consultant_at_discharge=Jane'
            },
            {
                'number': 2,
                '% Confirmed Diagnosis': 100,
                'Consultant': u'Ben',
                'Total Number of Patients': 1,
                'Consultant__link': u'/wardround/#/consultantreview?consultant_at_discharge=Ben'
            },
            {
                'number': '-',
                'Consultant': u'No Episodes',
                'Total Number of Patients': 0,
                'Consultant__link': u'/wardround/#/consultantreview?consultant_at_discharge=No+Episodes'
            },
        ]

        self.assertEqual(result, expected)
