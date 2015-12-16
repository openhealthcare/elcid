# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import datetime


def add_when(apps, schema_editor):
    MicrobiologyInput = apps.get_model("elcid", "MicrobiologyInput")

    for microbiology_input in MicrobiologyInput.objects.all():
        d = microbiology_input.date
        if d is not None:
            microbiology_input.when = datetime.combine(d, datetime.min.time())
            microbiology_input.save()


def reverse_when(apps, schema_editor):
    MicrobiologyInput = apps.get_model("elcid", "MicrobiologyInput")

    for microbiology_input in MicrobiologyInput.objects.all():
        c = microbiology_input.when

        if c is not None:
            microbiology_input.date = c.date()
            microbiology_input.save()

class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0005_microbiologyinput_when'),
    ]

    operations = [
        migrations.RunPython(
            add_when, reverse_code=reverse_when
        ),
    ]
