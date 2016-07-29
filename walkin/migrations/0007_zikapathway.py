# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0006_auto_20151109_1232'),
        ('walkin', '0006_auto_20151109_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZikaPathway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('pregnant', models.BooleanField(default=False)),
                ('gestation', models.CharField(max_length=255, null=True, blank=True)),
                ('due_date', models.CharField(max_length=255, null=True, blank=True)),
                ('antenatal_hospital', models.CharField(max_length=255, null=True, blank=True)),
                ('yellow_fever', models.CharField(max_length=255, null=True, blank=True)),
                ('advice', models.TextField(null=True, blank=True)),
                ('follow_up', models.TextField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_walkin_zikapathway_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_walkin_zikapathway_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
