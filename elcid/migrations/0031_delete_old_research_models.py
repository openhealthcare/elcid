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
        ('elcid', '0030_move_models_to_research'),
        ('research', '0004_migrate_content_types'),
    ]

    state_operations = [
        migrations.DeleteModel(name=i) for i in model_names
    ]

    operations = [
        # After this state operation, the Django DB state should match the
        # actual database structure.
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
