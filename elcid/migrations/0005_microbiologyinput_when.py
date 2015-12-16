# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0011_opatlineassessment_cm_from_exit_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='microbiologyinput',
            name='when',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
