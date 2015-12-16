# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0003_auto_20150922_1825'),
        ('elcid', '0010_add_micro_haem_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='HaemChemotherapyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Chemotherapy type',
            },
        ),
        migrations.CreateModel(
            name='HaemInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('date_of_transplant', models.DateField(null=True, blank=True)),
                ('neutropenia_onset', models.DateField(null=True, blank=True)),
                ('date_of_chemotherapy', models.DateField(null=True, blank=True)),
                ('count_recovery', models.DateField(null=True, blank=True)),
                ('patient_type_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('type_of_chemotherapy_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_elcid_haeminformation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('details', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HaemInformationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HaemTransplantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Transplant Type',
            },
        ),
        migrations.AddField(
            model_name='haeminformation',
            name='patient_type_fk',
            field=models.ForeignKey(blank=True, to='elcid.HaemInformationType', null=True),
        ),
        migrations.AddField(
            model_name='haeminformation',
            name='type_of_chemotherapy_fk',
            field=models.ForeignKey(blank=True, to='elcid.HaemChemotherapyType', null=True),
        ),
        migrations.AddField(
            model_name='haeminformation',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_haeminformation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
