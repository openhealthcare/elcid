# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


MICROHAEM_INFORMATION_TYPES = ["Other", "Transplant", "White cell"]


def add(apps, schema_editor):
    it = apps.get_model("elcid", "HaemInformationType")

    for t in MICROHAEM_INFORMATION_TYPES:
        it.objects.get_or_create(name=t)


def remove(apps, schema_editor):
    it = apps.get_model("elcid", "HaemInformationType")
    it.objects.filter(
        name__in=MICROHAEM_INFORMATION_TYPES
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0011_auto_20151008_1209'),
    ]

    operations = [
        migrations.RunPython(
            add, reverse_code=remove
        )
    ]
