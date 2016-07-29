# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

model_names = [
    "HaemChemotherapyType", "HaemTransplantType", "HaemInformationType",
    "EpisodeOfNeutropenia", "HaemInformation",
]


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0031_delete_old_research_models'),
    ]

    database_operations = [
        migrations.AlterModelTable(i, "microhaem_%s" % i.lower()) for i in model_names
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations
            )
    ]
