# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0023_duplicatepatient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='neutropeniainformation',
            options={'ordering': ['-start']},
        ),
    ]
