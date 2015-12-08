# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import opal.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0006_auto_20151109_1232'),
        ('elcid', '0029_auto_20151123_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='Infection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('site', models.CharField(max_length=255, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_elcid_infection_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('source', models.ManyToManyField(to='opal.Symptom')),
                ('updated_by', models.ForeignKey(related_name='updated_elcid_infection_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LiverFunction',
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
            name='LocationCategory',
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
            name='MedicalProcedure',
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
            name='Procedure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('date', models.DateField()),
                ('surgical_procedure_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('medical_procedure_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_elcid_procedure_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('medical_procedure_fk', models.ForeignKey(blank=True, to='elcid.MedicalProcedure', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Provenance',
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
            name='RenalFunction',
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
            name='SurgicalProcedure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='location',
            name='category',
        ),
        migrations.RemoveField(
            model_name='location',
            name='opat_acceptance',
        ),
        migrations.RemoveField(
            model_name='location',
            name='opat_discharge',
        ),
        migrations.RemoveField(
            model_name='location',
            name='opat_referral',
        ),
        migrations.RemoveField(
            model_name='location',
            name='opat_referral_consultant',
        ),
        migrations.RemoveField(
            model_name='location',
            name='opat_referral_route',
        ),
        migrations.RemoveField(
            model_name='location',
            name='opat_referral_team',
        ),
        migrations.RemoveField(
            model_name='location',
            name='opat_referral_team_address',
        ),
        migrations.AddField(
            model_name='line',
            name='button_hole',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='location',
            name='category_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='provenance_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='c_reactive_protein',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='liver_function_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='maximum_temperature',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='renal_function_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='white_cell_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='procedure',
            name='surgical_procedure_fk',
            field=models.ForeignKey(blank=True, to='elcid.SurgicalProcedure', null=True),
        ),
        migrations.AddField(
            model_name='procedure',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_procedure_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='category_fk',
            field=models.ForeignKey(blank=True, to='elcid.LocationCategory', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='provenance_fk',
            field=models.ForeignKey(blank=True, to='elcid.Provenance', null=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='liver_function_fk',
            field=models.ForeignKey(blank=True, to='elcid.LiverFunction', null=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='renal_function_fk',
            field=models.ForeignKey(blank=True, to='elcid.RenalFunction', null=True),
        ),
    ]
