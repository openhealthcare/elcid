# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0004_auto_20150907_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='microbiologyinput',
            name='date',
        ),
    ]
