# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_forwards(apps, schema_editor):
    Demographics = apps.get_model("elcid", "Demographics")

    for demographic in Demographics.objects.all():
        demographic.ethnicity_ft = demographic.ethnicity_old
        demographic.sex_ft = demographic.gender

        names = demographic.name.split(" ")

        if len(names) == 1:
            demographic.surname = names[0]
        else:
            demographic.first_name = names[0]
            demographic.surname = " ".join(names[1:])

        demographic.save()


def migrate_backwards(apps, schema_editor):
    Demographics = apps.get_model("elcid", "Demographics")

    for demographic in Demographics.objects.all():
        demographic.ethnicity_old = demographic.ethnicity_ft
        demographic.gender = demographic.sex_ft
        names = [
            demographic.first_name,
            demographic.middle_name,
            demographic.last_name
        ]

        demographic.name = " ".join(i for i in names if i)
        demographic.save()


class Migration(migrations.Migration):
    dependencies = [
        ('elcid', '0034_gloss_demographics_fields'),
    ]

    operations = [
        migrations.RunPython(
            migrate_forwards, reverse_code=migrate_backwards
        )
    ]
