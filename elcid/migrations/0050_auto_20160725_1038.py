# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0049_auto_20160510_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_with',
            field=models.CharField(max_length=200, null=True, verbose_name=b'With', blank=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='external_length',
            field=models.CharField(max_length=255, null=True, verbose_name=b'External Length When Inserted', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_acceptance',
            field=models.DateField(null=True, verbose_name=b'Referring consultant', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral',
            field=models.DateField(null=True, verbose_name=b'Date of referral to OPAT', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral_team',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Referring team', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral_team_address',
            field=models.TextField(null=True, verbose_name=b'Referring team address', blank=True),
        ),
    ]
