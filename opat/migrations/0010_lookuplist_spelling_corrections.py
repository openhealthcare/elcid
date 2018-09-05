# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-19 10:11
from __future__ import unicode_literals

from django.db import migrations

MAPPINGS = {
    ('opal', 'Line_complication',): {
        "Infection - Phelbitis": "Infection - Phlebitis"
    },
    ('opal', 'Antimicrobial_adverse_event',): {
        "Esosinophilia": "Eosinophilia"
    }
}


def forward(apps, *args, **kwargs):
    for model, translations in MAPPINGS.items():
        some_model = apps.get_model(*model)
        for from_translation, to_translation in translations.items():
            some_model.objects.filter(
                name=from_translation
            ).update(
                name=to_translation
            )


def backwards(apps, *args, **kwargs):
    for model, translations in MAPPINGS.items():
        some_model = apps.get_model(*model)
        for from_translation, to_translation in translations.items():
            some_model.objects.filter(
                name=to_translation
            ).update(
                name=from_translation
            )


class Migration(migrations.Migration):

    dependencies = [
        ('opat', '0009_auto_20180817_2042'),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=backwards)
    ]
