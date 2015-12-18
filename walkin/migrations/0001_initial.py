# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClinicalFindings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('lymphadenopathy', models.CharField(max_length=20, null=True, blank=True)),
                ('lymphadenopathy_details', models.CharField(max_length=255, null=True, blank=True)),
                ('jaundice', models.CharField(max_length=20, blank=True)),
                ('dehydrated', models.CharField(max_length=20, blank=True)),
                ('rash', models.CharField(max_length=20, blank=True)),
                ('cardiovascular', models.CharField(max_length=255, null=True, blank=True)),
                ('respiratory', models.CharField(max_length=255, null=True, blank=True)),
                ('abdominal', models.CharField(max_length=255, null=True, blank=True)),
                ('oropharnyx', models.CharField(max_length=255, null=True, blank=True)),
                ('neurological', models.CharField(max_length=255, null=True, blank=True)),
                ('other_findings', models.CharField(max_length=255, null=True, blank=True)),
                ('rash_type_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('rash_distribution_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Findings_rash_distribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Findings_rash_type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Management',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('date_of_appointment', models.DateField(null=True, blank=True)),
                ('advice', models.CharField(max_length=255, null=True, blank=True)),
                ('results_actioned', models.CharField(max_length=255, null=True, blank=True)),
                ('follow_up_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('follow_up_clinic_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Management_clinics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Management_follow_up',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('duration', models.CharField(max_length=255, null=True, blank=True)),
                ('details', models.CharField(max_length=255, null=True, blank=True)),
                ('onset', models.CharField(max_length=255, null=True, blank=True)),
                ('symptom_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('symptom_fk', models.ForeignKey(blank=True, to='opal.Symptom', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='WalkinNurseLedCare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('treatment', models.TextField(null=True, blank=True)),
                ('reason_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Wi_nurse_reason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='walkinnurseledcare',
            name='reason_fk',
            field=models.ForeignKey(blank=True, to='walkin.Wi_nurse_reason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='management',
            name='follow_up_clinic_fk',
            field=models.ForeignKey(blank=True, to='walkin.Management_clinics', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='management',
            name='follow_up_fk',
            field=models.ForeignKey(blank=True, to='walkin.Management_follow_up', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clinicalfindings',
            name='rash_distribution_fk',
            field=models.ForeignKey(blank=True, to='walkin.Findings_rash_distribution', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clinicalfindings',
            name='rash_type_fk',
            field=models.ForeignKey(blank=True, to='walkin.Findings_rash_type', null=True),
            preserve_default=True,
        ),
    ]
