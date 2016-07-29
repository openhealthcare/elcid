# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0046_demographics_death_indicator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographics',
            name='gp_practice_code',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='middle_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='post_code',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='religion',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
