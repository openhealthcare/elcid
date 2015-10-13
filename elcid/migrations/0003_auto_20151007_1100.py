# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0002_travel_did_not_travel'),
    ]

    operations = [
        migrations.AddField(
            model_name='opatoutcome',
            name='opat_outcome',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatoutcome',
            name='outcome_stage',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatoutcome',
            name='patient_outcome',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='carers',
            name='gp',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='carers',
            name='nurse',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pastmedicalhistory',
            name='year',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
