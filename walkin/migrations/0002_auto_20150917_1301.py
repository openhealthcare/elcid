# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('walkin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='findings_rash_distribution',
            options={'verbose_name': 'Findings rash distribution'},
        ),
        migrations.AlterModelOptions(
            name='findings_rash_type',
            options={'verbose_name': 'Findings rash type'},
        ),
        migrations.AlterModelOptions(
            name='management_clinics',
            options={'verbose_name': 'Management clinics', 'verbose_name_plural': 'Management clinics'},
        ),
        migrations.AlterModelOptions(
            name='management_follow_up',
            options={'verbose_name': 'Management follow up'},
        ),
        migrations.AlterModelOptions(
            name='wi_nurse_reason',
            options={'verbose_name': 'Walkin nurse reason'},
        ),
        migrations.AddField(
            model_name='clinicalfindings',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='clinicalfindings',
            name='created_by',
            field=models.ForeignKey(related_name='created_walkin_clinicalfindings_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='clinicalfindings',
            name='updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='clinicalfindings',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_walkin_clinicalfindings_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='management',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='management',
            name='created_by',
            field=models.ForeignKey(related_name='created_walkin_management_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='management',
            name='updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='management',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_walkin_management_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='symptom',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='symptom',
            name='created_by',
            field=models.ForeignKey(related_name='created_walkin_symptom_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='symptom',
            name='updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='symptom',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_walkin_symptom_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='walkinnurseledcare',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='walkinnurseledcare',
            name='created_by',
            field=models.ForeignKey(related_name='created_walkin_walkinnurseledcare_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='walkinnurseledcare',
            name='updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='walkinnurseledcare',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_walkin_walkinnurseledcare_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
