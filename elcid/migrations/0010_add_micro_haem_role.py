# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from microhaem.constants import MICROHAEM_ROLE


def add(apps, schema_editor):
    Role = apps.get_model("opal", "Role")
    Role.objects.get_or_create(
        name=MICROHAEM_ROLE
    )


def remove(apps, schema_editor):
    Role = apps.get_model("opal", "Role")
    Role.objects.filter(
        name=MICROHAEM_ROLE
    ).delete()



class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0009_microbiologytest_alert_investigation'),
    ]

    operations = [
        migrations.RunPython(
            add, reverse_code=remove
        )
    ]
