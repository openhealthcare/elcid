# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0008_add_micro_haem_clinical_interaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='microbiologytest',
            name='alert_investigation',
            field=models.BooleanField(default=False),
        ),
    ]
