# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0047_auto_20160405_0919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allergies',
            name='allergy_type',
        ),
    ]
