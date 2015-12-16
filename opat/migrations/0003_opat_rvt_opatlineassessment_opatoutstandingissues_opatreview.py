# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import opal.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elcid', '0028_move_models_to_opat'),
        ('opat', '0002_opatdressingtype'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='Opat_rvt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'verbose_name': 'OPAT RVT',
            },
        ),
        migrations.CreateModel(
            name='OPATLineAssessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('line', models.CharField(max_length=200, null=True, blank=True)),
                ('assessment_date', models.DateField(null=True, blank=True)),
                ('vip_score', models.IntegerField(null=True, blank=True)),
                ('dressing_type', models.CharField(max_length=200, null=True, blank=True)),
                ('dressing_change_date', models.DateField(null=True, blank=True)),
                ('dressing_change_reason', models.CharField(max_length=200, null=True, blank=True)),
                ('next_bionector_date', models.DateField(null=True, blank=True)),
                ('bionector_change_date', models.DateField(null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('dressing_intact', models.NullBooleanField(default=False)),
                ('lumen_flush_ok', models.NullBooleanField(default=False)),
                ('blood_drawback_seen', models.NullBooleanField(default=False)),
                ('cm_from_exit_site', models.FloatField(default=False)),
                ('created_by', models.ForeignKey(related_name='created_opat_opatlineassessment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_opat_opatlineassessment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'OPAT line assessment',
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OPATOutstandingIssues',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('details', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(related_name='created_opat_opatoutstandingissues_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_opat_opatoutstandingissues_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'OPAT outstanding issue',
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OPATReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('datetime', models.DateTimeField(null=True, blank=True)),
                ('initials', models.CharField(max_length=255, blank=True)),
                ('discussion', models.TextField(null=True, blank=True)),
                ('opat_plan', models.TextField(blank=True)),
                ('next_review', models.DateField(null=True, blank=True)),
                ('dressing_changed', models.NullBooleanField(default=False)),
                ('bung_changed', models.NullBooleanField(default=False)),
                ('medication_administered', models.TextField(null=True, blank=True)),
                ('rv_type_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('adverse_events_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('adverse_events_fk', models.ForeignKey(blank=True, to='opal.Antimicrobial_adverse_event', null=True)),
                ('created_by', models.ForeignKey(related_name='created_opat_opatreview_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('rv_type_fk', models.ForeignKey(blank=True, to='opat.Opat_rvt', null=True)),
                ('updated_by', models.ForeignKey(related_name='updated_opat_opatreview_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'OPAT review',
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OPATMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('review_date', models.DateField(null=True, blank=True)),
                ('reason_for_stopping', models.CharField(max_length=200, null=True, blank=True)),
                ('stopping_iv_details', models.CharField(max_length=200, null=True, blank=True)),
                ('treatment_outcome', models.CharField(max_length=200, null=True, blank=True)),
                ('deceased', models.NullBooleanField(default=False)),
                ('death_category', models.CharField(max_length=200, null=True, blank=True)),
                ('cause_of_death', models.CharField(max_length=200, null=True, blank=True)),
                ('readmitted', models.NullBooleanField(default=False)),
                ('readmission_cause', models.CharField(max_length=200, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('unplanned_stop_reason_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_opat_opatmeta_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
            ],
            options={
                'verbose_name': 'OPAT meta',
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OPATOutcome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('outcome_stage', models.CharField(max_length=200, null=True, blank=True)),
                ('treatment_outcome', models.CharField(max_length=200, null=True, blank=True)),
                ('patient_outcome', models.CharField(max_length=200, null=True, blank=True)),
                ('opat_outcome', models.CharField(max_length=200, null=True, blank=True)),
                ('deceased', models.NullBooleanField(default=False)),
                ('death_category', models.CharField(max_length=200, null=True, blank=True)),
                ('cause_of_death', models.CharField(max_length=200, null=True, blank=True)),
                ('readmitted', models.NullBooleanField(default=False)),
                ('readmission_cause', models.CharField(max_length=200, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('patient_feedback', models.NullBooleanField(default=False)),
                ('infective_diagnosis_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_opat_opatoutcome_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('infective_diagnosis_fk', models.ForeignKey(blank=True, to='opat.OPATInfectiveDiagnosis', null=True)),
                ('updated_by', models.ForeignKey(related_name='updated_opat_opatoutcome_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'OPAT outcome',
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OPATRejection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('decided_by', models.CharField(max_length=255, null=True, blank=True)),
                ('patient_choice', models.NullBooleanField(default=False)),
                ('oral_available', models.NullBooleanField(default=False)),
                ('not_needed', models.NullBooleanField(default=False)),
                ('patient_suitability', models.NullBooleanField(default=False)),
                ('not_fit_for_discharge', models.NullBooleanField(default=False)),
                ('non_complex_infection', models.NullBooleanField(default=False)),
                ('no_social_support', models.NullBooleanField(default=False)),
                ('reason', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_opat_opatrejection_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_opat_opatrejection_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'OPAT rejection',
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Unplanned_stop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Unplanned stop',
            },
        ),
        migrations.AddField(
            model_name='opatmeta',
            name='unplanned_stop_reason_fk',
            field=models.ForeignKey(blank=True, to='opat.Unplanned_stop', null=True),
        ),
        migrations.AddField(
            model_name='opatmeta',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_opat_opatmeta_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

    operations = [
        # After this state operation, the Django DB state should match the
        # actual database structure.
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
