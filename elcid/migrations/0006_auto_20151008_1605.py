# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opat', '0001_initial'),
        ('elcid', '0005_auto_20151007_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='opatoutcome',
            name='infective_diagnosis_fk',
            field=models.ForeignKey(blank=True, to='opat.OPATInfectiveDiagnosis', null=True),
        ),
        migrations.AddField(
            model_name='opatoutcome',
            name='infective_diagnosis_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
