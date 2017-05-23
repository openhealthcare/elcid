# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_forwards(apps, schema_editor):
    Diagnosis = apps.get_model("elcid", "Diagnosis")
    d = Diagnosis.objects.filter(provisional=None)
    d.update(provisional=False)


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0054_auto_20170321_1325'),
    ]

    operations = [
        migrations.RunPython(
            migrate_forwards
        )
    ]
