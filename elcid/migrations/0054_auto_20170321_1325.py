# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0053_auto_20170317_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographics',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name=b'Date of Birth', blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='date_of_death',
            field=models.DateField(null=True, verbose_name=b'Date of Death', blank=True),
        ),
    ]
