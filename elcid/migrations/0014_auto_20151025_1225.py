# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0013_auto_20151008_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primarydiagnosis',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
