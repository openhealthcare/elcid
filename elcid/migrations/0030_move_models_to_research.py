# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

model_names = [
    "Specimin", "LabtestDetails", "Organism_details", "Checkpoints_assay",
    "Antimicrobial_susceptability", "Specimin_appearance",
    "LabSpecimin", "LabTest", "RidRTIStudyDiagnosis",
    "RidRTITest", "CheckpointsAssay"
]

class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0029_auto_20151215_2310'),
    ]

    database_operations = [
        migrations.AlterModelTable(i, "research_%s" % i.lower()) for i in model_names
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations
            )
    ]
