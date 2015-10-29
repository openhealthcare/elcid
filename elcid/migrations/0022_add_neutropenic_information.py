# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


def create(apps, schema_editor):
    Patient = apps.get_model("opal", "Patient")
    NeutropeniaInformation = apps.get_model("elcid", "NeutropeniaInformation")
    patients = Patient.objects.all()
    neutropenic_information = [NeutropeniaInformation(patient=patient) for patient in patients]
    NeutropeniaInformation.objects.bulk_create(neutropenic_information)


def remove(apps, schema_editor):
    NeutropeniaInformation = apps.get_model("elcid", "NeutropeniaInformation")
    NeutropeniaInformation.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0021_neutropeniainformation'),
    ]

    operations = [
        migrations.RunPython(create, reverse_code=remove)
    ]
