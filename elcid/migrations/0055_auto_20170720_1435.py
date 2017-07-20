# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0054_auto_20170321_1325'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pastmedicalhistory',
            options={'verbose_name_plural': 'Past medical histories'},
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_with',
            field=models.CharField(null=True, blank=True, verbose_name='With', max_length=200),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='address_line1',
            field=models.CharField(null=True, blank=True, verbose_name='Address line 1', max_length=45),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='address_line2',
            field=models.CharField(null=True, blank=True, verbose_name='Address line 2', max_length=45),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='county',
            field=models.CharField(null=True, blank=True, verbose_name='County', max_length=40),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='post_code',
            field=models.CharField(null=True, blank=True, verbose_name='Post Code', max_length=10),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='death_indicator',
            field=models.BooleanField(help_text=b'This field will be True if the patient is deceased.', default=False),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='hospital_number',
            field=models.CharField(help_text=b'The unique identifier for this patient at the hospital.', blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='provisional',
            field=models.BooleanField(help_text=b'True if the diagnosis is provisional. Defaults to False', verbose_name=b'Provisional?', default=False),
        ),
        migrations.AlterField(
            model_name='line',
            name='external_length',
            field=models.CharField(null=True, blank=True, verbose_name='External Length When Inserted', max_length=255),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_acceptance',
            field=models.DateField(blank=True, verbose_name='Date Of Acceptance To OPAT', null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral',
            field=models.DateField(blank=True, verbose_name='Date Of Referral To OPAT', null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral_consultant',
            field=models.CharField(null=True, blank=True, verbose_name='Referring Consultant', max_length=255),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral_team',
            field=models.CharField(null=True, blank=True, verbose_name='Referring Team', max_length=255),
        ),
        migrations.AlterField(
            model_name='location',
            name='opat_referral_team_address',
            field=models.TextField(blank=True, verbose_name='Referring team address', null=True),
        ),
        migrations.AlterField(
            model_name='microbiologyinput',
            name='initials',
            field=models.CharField(blank=True, verbose_name='Advice given by', max_length=255),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='scrub_typhus_igg',
            field=models.CharField(blank=True, verbose_name='Scrub Typhus IgG', max_length=20),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='scrub_typhus_igm',
            field=models.CharField(blank=True, verbose_name='Scrub Typhus IgM', max_length=20),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='spotted_fever_igg',
            field=models.CharField(blank=True, verbose_name='Spotted Fever Group IgG', max_length=20),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='spotted_fever_igm',
            field=models.CharField(blank=True, verbose_name='Spotted Fever Group IgM', max_length=20),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='typhus_group_igg',
            field=models.CharField(blank=True, verbose_name='Typhus Group IgG', max_length=20),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='typhus_group_igm',
            field=models.CharField(blank=True, verbose_name='Typhus Group IgM', max_length=20),
        ),
        migrations.AlterField(
            model_name='presentingcomplaint',
            name='duration',
            field=models.CharField(help_text='The duration for which the patient had been experiencing these symptoms when recorded.', blank=True, null=True, max_length=255, choices=[('3 days or less', '3 days or less'), ('4-10 days', '4-10 days'), ('11-21 days', '11-21 days'), ('22 days to 3 months', '22 days to 3 months'), ('over 3 months', 'over 3 months')]),
        ),
    ]
