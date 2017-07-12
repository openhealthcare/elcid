import datetime

from opal.core.test import OpalTestCase
from opal.models import Episode

from infectiousdiseases.reports import IdLiasonReport


class IdLiasonReportTestCase(OpalTestCase):
    def setUp(self):
        self.report = IdLiasonReport()

    def test_get_queryset_vanilla(self):
        _, e1 = self.new_patient_and_episode_please()
        e1.discharge_date = datetime.date(2017, 5, 5)
        e1.tagging_set.create(
            value="id_liaison",
            archived=True,
        )
        e1.save()

        _, e2 = self.new_patient_and_episode_please()
        e2.discharge_date = datetime.date(2017, 5, 5)

        e2.tagging_set.create(
            value="something_else",
            archived=True,
        )
        e2.save()
        result = self.report.get_queryset(datetime.date(2017, 5, 1))
        self.assertEqual(
            list(result), list(Episode.objects.filter(id=e1.id))
        )
