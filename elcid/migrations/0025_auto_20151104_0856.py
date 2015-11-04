# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0004_merge'),
        ('elcid', '0024_auto_20151030_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodOfNeutropenia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('start', models.DateField(null=True, blank=True)),
                ('stop', models.DateField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_elcid_periodofneutropenia_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_elcid_periodofneutropenia_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-start'],
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='neutropeniainformation',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='neutropeniainformation',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='neutropeniainformation',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='NeutropeniaInformation',
        ),
    ]
