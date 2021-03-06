# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-03 14:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('walkin', '0011_auto_20170720_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicalfindings',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_walkin_clinicalfindings_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='clinicalfindings',
            name='rash_distribution_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='walkin.Findings_rash_distribution'),
        ),
        migrations.AlterField(
            model_name='clinicalfindings',
            name='rash_type_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='walkin.Findings_rash_type'),
        ),
        migrations.AlterField(
            model_name='clinicalfindings',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_walkin_clinicalfindings_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='management',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_walkin_management_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='management',
            name='follow_up_clinic_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='walkin.Management_clinics'),
        ),
        migrations.AlterField(
            model_name='management',
            name='follow_up_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='walkin.Management_follow_up'),
        ),
        migrations.AlterField(
            model_name='management',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_walkin_management_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_walkin_symptom_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='symptom_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='opal.Symptom'),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_walkin_symptom_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='walkinnurseledcare',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_walkin_walkinnurseledcare_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='walkinnurseledcare',
            name='reason_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='walkin.Wi_nurse_reason'),
        ),
        migrations.AlterField(
            model_name='walkinnurseledcare',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_walkin_walkinnurseledcare_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='zikapathway',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_walkin_zikapathway_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='zikapathway',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_walkin_zikapathway_subrecords', to=settings.AUTH_USER_MODEL),
        ),
    ]
