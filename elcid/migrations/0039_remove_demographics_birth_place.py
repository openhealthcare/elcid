# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0038_demographics_sourced_from_upstream'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demographics',
            name='birth_place',
        ),
    ]
