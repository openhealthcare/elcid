# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations
from elcid.constants import MICROHAEM_CONSULTATIONS


def add(apps, schema_editor):
    ReasonForInteraction = apps.get_model("opal", "Clinical_advice_reason_for_interaction")

    for micro_haem_consulation in MICROHAEM_CONSULTATIONS:
        ReasonForInteraction.objects.create(name=micro_haem_consulation)


def remove(apps, schema_editor):
    ReasonForInteraction = apps.get_model(
        "opal", "Clinical_advice_reason_for_interaction"
    )
    ReasonForInteraction.objects.filter(
        name__in=MICROHAEM_CONSULTATIONS
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0007_remove_microbiologyinput_date'),
    ]

    operations = [
        migrations.RunPython(
            add, reverse_code=remove
        ),
    ]
