"""
Unittests for elcid.management.commands.randomise_admission_dates
"""
import datetime

from opal.core.test import OpalTestCase
from opal.models import Episode, Patient

from elcid.management.commands import randomise_admission_dates

class RandomiseAdmissionDates(OpalTestCase):

    def test_handle(self):
        p = Patient.objects.create()
        e = Episode.objects.create(date_of_admission=datetime.date(1988, 1, 1),
                                   patient=p)

        c = randomise_admission_dates.Command()
        c.handle()
        eafter = Episode.objects.get(id=e.id)
        self.assertEqual(2014, eafter.date_of_admission.year)
