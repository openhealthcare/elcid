# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0008_opatdressingtype'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OPATDressingType',
        ),
    ]
