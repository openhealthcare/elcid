# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0019_auto_20151026_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentingcomplaint',
            name='symptoms',
            field=models.ManyToManyField(related_name='presenting_complaints', to='opal.Symptom'),
        ),
        migrations.AlterField(
            model_name='presentingcomplaint',
            name='details',
            field=models.TextField(null=True, blank=True),
        ),
    ]
