# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='TropicalLiasonMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('external_hospital_number', models.CharField(max_length=256)),
                ('hospital', models.CharField(max_length=256)),
                ('hospital_contact', models.CharField(max_length=256)),
                ('contact_telephone_number', models.CharField(max_length=256)),
                ('contact_email_address', models.CharField(max_length=256)),
                ('created_by', models.ForeignKey(related_name='created_infectiousdiseases_tropicalliasonmeta_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_infectiousdiseases_tropicalliasonmeta_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
    ]
