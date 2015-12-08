# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0030_auto_20151203_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfectionSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='infection',
            name='source',
        ),
        migrations.AddField(
            model_name='infection',
            name='source_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='infection',
            name='source_fk',
            field=models.ForeignKey(blank=True, to='elcid.InfectionSource', null=True),
        ),
    ]
