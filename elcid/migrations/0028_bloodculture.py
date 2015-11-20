# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0006_auto_20151109_1232'),
        ('elcid', '0027_ridrtistudydiagnosis'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodCulture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('date_ordered', models.DateField(null=True, blank=True)),
                ('details', models.CharField(max_length=255, blank=True)),
                ('microscopy', models.CharField(max_length=255, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_elcid_bloodculture_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('organisms', models.ManyToManyField(to='opal.Microbiology_organism')),
                ('resistant_antibiotics', models.ManyToManyField(related_name='blood_culture_resistant', to='opal.Antimicrobial')),
                ('sensitive_antibiotics', models.ManyToManyField(related_name='blood_culture_sensitive', to='opal.Antimicrobial')),
                ('updated_by', models.ForeignKey(related_name='updated_elcid_bloodculture_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
