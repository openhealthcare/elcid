# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchStudy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('clinical_lead', models.ManyToManyField(related_name=b'clinical_lead_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('research_nurse', models.ManyToManyField(related_name=b'research_nurse_user', null=True, verbose_name=b'Research Practitioner', to=settings.AUTH_USER_MODEL, blank=True)),
                ('researcher', models.ManyToManyField(related_name=b'researcher_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('scientist', models.ManyToManyField(related_name=b'scientist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Research Studies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudyParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('study_id', models.CharField(max_length=200, null=True, blank=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
