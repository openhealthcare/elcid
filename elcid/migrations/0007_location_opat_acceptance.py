# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0006_auto_20151008_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='opat_acceptance',
            field=models.DateField(null=True, blank=True),
        ),
    ]
