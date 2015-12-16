# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0018_auto_20151026_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentingcomplaint',
            name='details',
            field=models.TextField(max_length=255, null=True, blank=True),
        ),
    ]
