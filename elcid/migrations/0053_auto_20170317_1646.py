# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0052_auto_20170301_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentingcomplaint',
            name='duration',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[(b'3 days or less', b'3 days or less'), (b'4-10 days', b'4-10 days'), (b'11-21 days', b'11-21 days'), (b'22 days to 3 months', b'22 days to 3 months'), (b'over 3 months', b'over 3 months')]),
        ),
    ]
