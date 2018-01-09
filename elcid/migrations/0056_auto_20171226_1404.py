# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0055_auto_20170720_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergies',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_allergies_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='allergies',
            name='drug_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Antimicrobial', null=True),
        ),
        migrations.AlterField(
            model_name='allergies',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_allergies_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='antimicrobial',
            name='adverse_event_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Antimicrobial_adverse_event', null=True),
        ),
        migrations.AlterField(
            model_name='antimicrobial',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_antimicrobial_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='antimicrobial',
            name='delivered_by_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='elcid.Drug_delivered', null=True),
        ),
        migrations.AlterField(
            model_name='antimicrobial',
            name='drug_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Antimicrobial', null=True),
        ),
        migrations.AlterField(
            model_name='antimicrobial',
            name='frequency_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Antimicrobial_frequency', null=True),
        ),
        migrations.AlterField(
            model_name='antimicrobial',
            name='reason_for_stopping_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='elcid.Iv_stop', null=True),
        ),
        migrations.AlterField(
            model_name='antimicrobial',
            name='route_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Antimicrobial_route', null=True),
        ),
        migrations.AlterField(
            model_name='antimicrobial',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_antimicrobial_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_appointment_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_appointment_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='carers',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_carers_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='carers',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_carers_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='consultantatdischarge',
            name='consultant_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='elcid.Consultant', null=True),
        ),
        migrations.AlterField(
            model_name='consultantatdischarge',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_consultantatdischarge_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='consultantatdischarge',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_consultantatdischarge_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_contactdetails_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_contactdetails_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='birth_place_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Destination', null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_demographics_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='ethnicity_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Ethnicity', null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='marital_status_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.MaritalStatus', null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='sex_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Gender', null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='title_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Title', null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_demographics_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='condition_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Condition', null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_diagnosis_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_diagnosis_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='duplicatepatient',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_duplicatepatient_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='duplicatepatient',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_duplicatepatient_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='generalnote',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_generalnote_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='generalnote',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_generalnote_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='complications_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Line_complication', null=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_line_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='line_type_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Line_type', null=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='removal_reason_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Line_removal_reason', null=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='site_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Line_site', null=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_line_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_location_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_location_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='microbiologyinput',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_microbiologyinput_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='microbiologyinput',
            name='reason_for_interaction_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Clinical_advice_reason_for_interaction', null=True),
        ),
        migrations.AlterField(
            model_name='microbiologyinput',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_microbiologyinput_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_microbiologytest_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='hiv_declined_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='elcid.Hiv_no', null=True),
        ),
        migrations.AlterField(
            model_name='microbiologytest',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_microbiologytest_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='pastmedicalhistory',
            name='condition_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Condition', null=True),
        ),
        migrations.AlterField(
            model_name='pastmedicalhistory',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_pastmedicalhistory_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='pastmedicalhistory',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_pastmedicalhistory_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='presentingcomplaint',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_presentingcomplaint_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='presentingcomplaint',
            name='symptom_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Symptom', null=True),
        ),
        migrations.AlterField(
            model_name='presentingcomplaint',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_presentingcomplaint_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='primarydiagnosis',
            name='condition_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Condition', null=True),
        ),
        migrations.AlterField(
            model_name='primarydiagnosis',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_primarydiagnosis_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='primarydiagnosis',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_primarydiagnosis_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_result_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_result_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='secondarydiagnosis',
            name='condition_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Condition', null=True),
        ),
        migrations.AlterField(
            model_name='secondarydiagnosis',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_secondarydiagnosis_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='secondarydiagnosis',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_secondarydiagnosis_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_todo_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_todo_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='travel',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_travel_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='travel',
            name='destination_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Destination', null=True),
        ),
        migrations.AlterField(
            model_name='travel',
            name='malaria_drug_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Antimicrobial', null=True),
        ),
        migrations.AlterField(
            model_name='travel',
            name='reason_for_travel_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opal.Travel_reason', null=True),
        ),
        migrations.AlterField(
            model_name='travel',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_travel_subrecords', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
