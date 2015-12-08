# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0031_auto_20151203_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedure',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
