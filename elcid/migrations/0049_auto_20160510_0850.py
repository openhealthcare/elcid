# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0048_remove_allergies_allergy_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allergies',
            name='sourced_from_upstream',
        ),
        migrations.RemoveField(
            model_name='demographics',
            name='sourced_from_upstream',
        ),
        migrations.AddField(
            model_name='allergies',
            name='external_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='external_system',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='external_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='external_system',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
