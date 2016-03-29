# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0041_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='allergies',
            name='allergen_reference',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='allergen_reference_system',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='allergy_description',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='allergy_reference_name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='allergy_start_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='allergy_type',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='allergy_type_description',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='certainty_description',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='certainty_id',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='diagnosis_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='no_allergies',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='allergies',
            name='status_description',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='status_id',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
