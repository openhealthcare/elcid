# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0036_move_elcid_data_to_gloss_format'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demographics',
            old_name='surname ',
            new_name='surname',
        ),
    ]
