# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def move_fields_to_gloss(apps, schema_editor):
    Demographics = apps.get_model("elcid", "Demographics")

    for demographics in Demographics.objects.all():
        names = demographics.name.split(" ")
        if len(names) == 1:
            demographics.surname = names[0]
        else:
            demographics.first_name = names[0]
            demographics.surname = " ".join(names[1:])

        demographics.ethnicity_ft = demographics.ethnicity_old
        demographics.sex_ft = demographics.gender
        demographics.save()


def move_fields_from_gloss(apps, schema_editor):
    Demographics = apps.get_model("elcid", "Demographics")

    for demographics in Demographics.objects.all():
        demographics.ethnicity_old = demographics.ethnicity_ft
        demographics.gender = demographics.sex_ft
        demographics.name = "{0} {1}".format(
            demographics.first_name, demographics.surname
        )
        demographics.save()


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0035_add_ethnicity_sex_fk_or_ft'),
    ]

    operations = [
        migrations.RunPython(
            move_fields_to_gloss, reverse_code=move_fields_from_gloss
        )
    ]
