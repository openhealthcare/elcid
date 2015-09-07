# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0002_travel_did_not_travel'),
    ]

    operations = [
        migrations.AddField(
            model_name='microbiologyinput',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='neutropenic',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='started_antibiotics',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='stopped_antibiotics',
            field=models.NullBooleanField(),
        ),
    ]
