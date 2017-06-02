# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_forwards(apps, schema_editor):
    Diagnosis = apps.get_model("elcid", "Diagnosis")
    d = Diagnosis.objects.filter(provisional=None)
    d.update(provisional=False)


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0050_auto_20160725_1038'),
    ]

    operations = [
        migrations.RunPython(
            migrate_forwards
        )
    ]
