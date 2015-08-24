# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='did_not_travel',
            field=models.NullBooleanField(default=False),
        ),
    ]
