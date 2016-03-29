# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0042_auto_20160325_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='allergies',
            name='sourced_from_upstream',
            field=models.BooleanField(default=False),
        ),
    ]
