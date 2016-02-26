# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walkin', '0007_zikapathway'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zikapathway',
            name='due_date',
        ),
    ]
