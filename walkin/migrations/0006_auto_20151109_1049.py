# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walkin', '0005_symptom_symptoms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptom',
            name='details',
            field=models.TextField(null=True, blank=True),
        ),
    ]
