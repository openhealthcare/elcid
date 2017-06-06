# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0051_auto_20160725_1222'),
        ('elcid', '0051_auto_20170523_0831'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pastmedicalhistory',
            options={},
        ),
        migrations.AlterField(
            model_name='demographics',
            name='gp_practice_code',
            field=models.CharField(max_length=20, null=True, verbose_name=b'GP Practice Code', blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='nhs_number',
            field=models.CharField(max_length=255, null=True, verbose_name=b'NHS Number', blank=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='provisional',
            field=models.BooleanField(default=False, verbose_name=b'Provisional?'),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='anti_hbcore_igg',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='anti_hbcore_igm',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='anti_hbs',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='ebna_igg',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='hbsag',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='hsv',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='igg',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='igm',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='rpr',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='tppa',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='vca_igg',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='vca_igm',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='vzv',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
