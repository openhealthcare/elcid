# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0002_travel_did_not_travel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastmedicalhistory',
            name='year',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
