# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walkin', '0010_zikapathway_date_leaving'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptom',
            name='duration',
            field=models.CharField(help_text='The duration for which the patient had been experiencing these symptoms when recorded.', blank=True, null=True, max_length=255),
        ),
    ]
