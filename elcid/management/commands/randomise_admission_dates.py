"""
Randomise our admission dates over the last year.
"""
import datetime
import random

from django.core.management.base import BaseCommand
from django.conf import settings

from opal.models import Episode

class Command(BaseCommand):

    def handle(self, *args, **options):
        twentyten = datetime.date(2010, 1, 1)

        for e in Episode.objects.filter(date_of_admission__lt=twentyten):
            year = 2014
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            e.date_of_admission = datetime.date(year, month, day)
            e.save()
