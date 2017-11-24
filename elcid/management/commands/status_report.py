
"""

"""
import datetime
import json
import logging

from django.core.management.base import BaseCommand
from opal.core import subrecords
from opal import models


class Command(BaseCommand):

    def count_created_last_week(self, model):
        today = datetime.datetime.combine(
            datetime.date.today(), datetime.time.min
        )
        last_week = today - datetime.timedelta(7)
        return model.objects.filter(created__gte=last_week).count()

    def handle(self, *args, **options):
        # we want to catch the output, so lets not output info level logging
        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.ERROR)
        result = dict(
            all_time=dict(
                Episode=models.Episode.objects.count()
            ),
            last_week=dict(
                Episode=self.count_created_last_week(models.Episode)
            )
        )

        for subrecord in subrecords.subrecords():
            count_all_time = subrecord.objects.count()
            count_last_week = self.count_created_last_week(subrecord)

            result["all_time"][subrecord.get_display_name()] = count_all_time
            result["last_week"][subrecord.get_display_name()] = count_last_week
        self.stdout.write(json.dumps(result, indent=4))
