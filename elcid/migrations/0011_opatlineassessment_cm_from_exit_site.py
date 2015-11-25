# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0010_auto_20151009_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='opatlineassessment',
            name='cm_from_exit_site',
            field=models.FloatField(default=False),
        ),
    ]
