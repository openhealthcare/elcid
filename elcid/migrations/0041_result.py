# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0012_maritalstatus_title'),
        ('elcid', '0040_auto_20160324_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('lab_number', models.CharField(max_length=255, null=True, blank=True)),
                ('profile_code', models.CharField(max_length=255, null=True, blank=True)),
                ('profile_description', models.CharField(max_length=255, null=True, blank=True)),
                ('request_datetime', models.DateTimeField(null=True, blank=True)),
                ('observation_datetime', models.DateTimeField(null=True, blank=True)),
                ('last_edited', models.DateTimeField(null=True, blank=True)),
                ('result_status', models.CharField(max_length=255, null=True, blank=True)),
                ('observations', jsonfield.fields.JSONField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_elcid_result_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_elcid_result_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
