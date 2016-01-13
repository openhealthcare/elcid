# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyparticipation',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studyparticipation',
            name='created_by',
            field=models.ForeignKey(related_name='created_research_studyparticipation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='studyparticipation',
            name='updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studyparticipation',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_research_studyparticipation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
