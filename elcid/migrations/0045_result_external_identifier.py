# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0044_auto_20160329_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='external_identifier',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
