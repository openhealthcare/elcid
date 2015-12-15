# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

model_names = [
    "OPATLineAssessment", "Opat_rvt", "OPATOutstandingIssues",
    "OPATReview", "OPATMeta", "OPATOutcome", "OPATRejection",
    "Unplanned_stop"
]


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0028_move_models_to_opat'),
        ('opat', '0005_migrate_data_from_elcid'),
    ]

    state_operations = [
        # Pasted from auto-generated operations in previous step:
        migrations.DeleteModel(name=i) for i in model_names
    ]

    operations = [
        # After this state operation, the Django DB state should match the
        # actual database structure.
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
