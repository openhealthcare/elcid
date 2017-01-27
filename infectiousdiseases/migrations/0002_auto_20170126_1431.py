# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('infectiousdiseases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalLiasonContactDetails',
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
                ('created_by', models.ForeignKey(related_name='created_infectiousdiseases_externalliasoncontactdetails_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_infectiousdiseases_externalliasoncontactdetails_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='tropicalliasonmeta',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='tropicalliasonmeta',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='tropicalliasonmeta',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='TropicalLiasonMeta',
        ),
    ]
