# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0009_delete_opatdressingtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='opatlineassessment',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatlineassessment',
            name='next_bionector_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='opatlineassessment',
            name='cm_from_exit_site',
            field=models.FloatField(default=False),
        ),
    ]
