# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0037_auto_20160324_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='demographics',
            name='sourced_from_upstream',
            field=models.BooleanField(default=False),
        ),
    ]
