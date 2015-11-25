# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0028_bloodculture'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodCultureSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bloodculture',
            name='anaerobic',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='bloodculture',
            name='date_positive',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bloodculture',
            name='source_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bloodculture',
            name='source_fk',
            field=models.ForeignKey(blank=True, to='elcid.BloodCultureSource', null=True),
        ),
    ]
