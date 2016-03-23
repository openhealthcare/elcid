# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0011_patientrecordaccess'),
        ('elcid', '0033_remove_microhaem_models'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demographics',
            old_name='ethnicity',
            new_name='ethnicity_old',
        ),
        migrations.AddField(
            model_name='demographics',
            name='birth_place',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='date_of_death',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='ethnicity_fk',
            field=models.ForeignKey(blank=True, to='opal.Ethnicity', null=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='ethnicity_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='first_name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='gp_practice_code',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='marital_status',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='middle_name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='post_code',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='religion',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='sex_fk',
            field=models.ForeignKey(blank=True, to='opal.Gender', null=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='sex_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='surname',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='title',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
