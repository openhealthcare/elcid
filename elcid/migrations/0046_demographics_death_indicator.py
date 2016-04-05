# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0045_result_external_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='demographics',
            name='death_indicator',
            field=models.BooleanField(default=False),
        ),
    ]
