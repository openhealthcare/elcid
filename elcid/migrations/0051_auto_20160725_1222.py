# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0050_auto_20160725_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='opat_acceptance',
            field=models.DateField(null=True, verbose_name=b'Referring Consultant', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral',
            field=models.DateField(null=True, verbose_name=b'Date Of Referral To OPAT', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral_consultant',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Referring Consultant', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral_team',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Referring Team', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologyinput',
            name='initials',
            field=models.CharField(max_length=255, verbose_name=b'Advice given by', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='anti_hbcore_igg',
            field=models.CharField(max_length=20, verbose_name=b'anti-HbCore IgG', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='anti_hbcore_igm',
            field=models.CharField(max_length=20, verbose_name=b'anti-HbCore IgM', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='anti_hbs',
            field=models.CharField(max_length=20, verbose_name=b'anti-HbS', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='ebna_igg',
            field=models.CharField(max_length=20, verbose_name=b'EBNA IgG', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='hbsag',
            field=models.CharField(max_length=20, verbose_name=b'HBsAg', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='hsv',
            field=models.CharField(max_length=20, verbose_name=b'HSV', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='igg',
            field=models.CharField(max_length=20, verbose_name=b'IgG', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='igm',
            field=models.CharField(max_length=20, verbose_name=b'IgM', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='rpr',
            field=models.CharField(max_length=20, verbose_name=b'RPR', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='scrub_typhus_igg',
            field=models.CharField(max_length=20, verbose_name=b'Scrub Typhus IgG', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='scrub_typhus_igm',
            field=models.CharField(max_length=20, verbose_name=b'Scrub Typhus IgM', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='spotted_fever_igg',
            field=models.CharField(max_length=20, verbose_name=b'Spotted Fever Group IgG', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='spotted_fever_igm',
            field=models.CharField(max_length=20, verbose_name=b'Spotted Fever Group IgM', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='tppa',
            field=models.CharField(max_length=20, verbose_name=b'TPPA', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='typhus_group_igg',
            field=models.CharField(max_length=20, verbose_name=b'Typhus Group IgG', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='typhus_group_igm',
            field=models.CharField(max_length=20, verbose_name=b'Typhus Group IgM', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='vca_igg',
            field=models.CharField(max_length=20, verbose_name=b'IgG', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='vca_igm',
            field=models.CharField(max_length=20, verbose_name=b'IgM', blank=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='vzv',
            field=models.CharField(max_length=20, verbose_name=b'VZV', blank=True),
        ),
    ]
