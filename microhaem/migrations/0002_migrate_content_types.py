# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from elcid.migrations.utils.copy_data import update_content_types


model_names = [
    "HaemChemotherapyType", "HaemTransplantType", "HaemInformationType",
    "EpisodeOfNeutropenia", "HaemInformation",
]

from_app = "elcid"
to_app = "microhaem"


def forward(apps, *args):
    for model_name in model_names:
        update_content_types(
            apps, from_app, model_name, to_app, model_name
        )


def backwards(apps, *args):
    for model_name in model_names:
        update_content_types(
            apps, to_app, model_name, from_app, model_name
        )


class Migration(migrations.Migration):

    dependencies = [
        ('microhaem', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=backwards)
    ]
