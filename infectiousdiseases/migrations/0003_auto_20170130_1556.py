# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infectiousdiseases', '0002_auto_20170126_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalliasoncontactdetails',
            name='contact_notes',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='externalliasoncontactdetails',
            name='contact_email_address',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='externalliasoncontactdetails',
            name='contact_telephone_number',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='externalliasoncontactdetails',
            name='external_hospital_number',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='externalliasoncontactdetails',
            name='hospital',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='externalliasoncontactdetails',
            name='hospital_contact',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
