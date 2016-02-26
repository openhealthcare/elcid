# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walkin', '0008_remove_zikapathway_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='zikapathway',
            name='due_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
