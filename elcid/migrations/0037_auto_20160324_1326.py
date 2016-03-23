# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0012_maritalstatus_title'),
        ('elcid', '0036_auto_20160324_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demographics',
            name='marital_status',
        ),
        migrations.RemoveField(
            model_name='demographics',
            name='title',
        ),
        migrations.AddField(
            model_name='demographics',
            name='marital_status_fk',
            field=models.ForeignKey(blank=True, to='opal.MaritalStatus', null=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='marital_status_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='title_fk',
            field=models.ForeignKey(blank=True, to='opal.Title', null=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='title_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
