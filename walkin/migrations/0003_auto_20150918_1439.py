# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walkin', '0002_auto_20150917_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinicalfindings',
            name='created',
        ),
        migrations.RemoveField(
            model_name='clinicalfindings',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='clinicalfindings',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='clinicalfindings',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='management',
            name='created',
        ),
        migrations.RemoveField(
            model_name='management',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='management',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='management',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='symptom',
            name='created',
        ),
        migrations.RemoveField(
            model_name='symptom',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='symptom',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='symptom',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='walkinnurseledcare',
            name='created',
        ),
        migrations.RemoveField(
            model_name='walkinnurseledcare',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='walkinnurseledcare',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='walkinnurseledcare',
            name='updated_by',
        ),
    ]
