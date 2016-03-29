# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0013_inpatientadmission'),
        ('elcid', '0043_allergies_sourced_from_upstream'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='episode',
        ),
        migrations.AddField(
            model_name='result',
            name='patient',
            field=models.ForeignKey(default=1, to='opal.Patient'),
            preserve_default=False,
        ),
    ]
