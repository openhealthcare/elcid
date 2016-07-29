# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

model_names = [
    "HaemChemotherapyType", "HaemTransplantType", "HaemInformationType",
    "EpisodeOfNeutropenia", "HaemInformation",
]


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0032_move_models_to_microhaem'),
        ('microhaem', '0002_migrate_content_types'),
    ]

    state_operations = [
        migrations.DeleteModel(name=i) for i in model_names
    ]

    operations = [
        # After this state operation, the Django DB state should match the
        # actual database structure.
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
