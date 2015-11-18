# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='microbiologytest',
            name='scrub_typhus_igg',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologytest',
            name='scrub_typhus_igm',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologytest',
            name='spotted_fever_igg',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologytest',
            name='spotted_fever_igm',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologytest',
            name='typhus_group_igg',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologytest',
            name='typhus_group_igm',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
