# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opat', '0004_migrate_data_from_elcid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opatmeta',
            options={'verbose_name': 'OPAT episode'},
        ),
    ]
