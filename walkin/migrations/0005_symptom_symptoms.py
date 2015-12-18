# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0004_merge'),
        ('walkin', '0004_auto_20150918_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='symptom',
            name='symptoms',
            field=models.ManyToManyField(related_name='walkin_symptoms', to='opal.Symptom'),
        ),
    ]
