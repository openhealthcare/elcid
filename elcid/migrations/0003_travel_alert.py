# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0002_travel_did_not_travel'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='alert',
            field=models.BooleanField(default=False),
        ),
    ]
