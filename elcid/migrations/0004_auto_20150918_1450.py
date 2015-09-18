# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elcid', '0003_auto_20150917_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='allergies',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_allergies_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='allergies',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_allergies_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='antimicrobial',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='antimicrobial',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_antimicrobial_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='antimicrobial',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='antimicrobial',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_antimicrobial_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_appointment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_appointment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='carers',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='carers',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_carers_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='carers',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='carers',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_carers_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='checkpointsassay',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='checkpointsassay',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_checkpointsassay_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='checkpointsassay',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='checkpointsassay',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_checkpointsassay_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_contactdetails_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_contactdetails_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_demographics_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='demographics',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_demographics_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_diagnosis_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_diagnosis_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='generalnote',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='generalnote',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_generalnote_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='generalnote',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='generalnote',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_generalnote_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='labspecimin',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='labspecimin',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_labspecimin_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='labspecimin',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='labspecimin',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_labspecimin_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_labtest_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_labtest_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='line',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='line',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_line_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='line',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='line',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_line_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_location_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_location_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_microbiologyinput_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologyinput',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_microbiologyinput_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='microbiologytest',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologytest',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_microbiologytest_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='microbiologytest',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='microbiologytest',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_microbiologytest_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatlineassessment',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatlineassessment',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_opatlineassessment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatlineassessment',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatlineassessment',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_opatlineassessment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatmeta',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatmeta',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_opatmeta_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatmeta',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatmeta',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_opatmeta_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatoutcome',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatoutcome',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_opatoutcome_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatoutcome',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatoutcome',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_opatoutcome_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatoutstandingissues',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatoutstandingissues',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_opatoutstandingissues_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatoutstandingissues',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatoutstandingissues',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_opatoutstandingissues_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatrejection',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatrejection',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_opatrejection_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatrejection',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatrejection',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_opatrejection_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatreview',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatreview',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_opatreview_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='opatreview',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opatreview',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_opatreview_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='pastmedicalhistory',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pastmedicalhistory',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_pastmedicalhistory_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='pastmedicalhistory',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pastmedicalhistory',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_pastmedicalhistory_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='presentingcomplaint',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='presentingcomplaint',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_presentingcomplaint_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='presentingcomplaint',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='presentingcomplaint',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_presentingcomplaint_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='primarydiagnosis',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='primarydiagnosis',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_primarydiagnosis_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='primarydiagnosis',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='primarydiagnosis',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_primarydiagnosis_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ridrtitest',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ridrtitest',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_ridrtitest_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ridrtitest',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ridrtitest',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_ridrtitest_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='secondarydiagnosis',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='secondarydiagnosis',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_secondarydiagnosis_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='secondarydiagnosis',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='secondarydiagnosis',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_secondarydiagnosis_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_todo_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_todo_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='travel',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='travel',
            name='created_by',
            field=models.ForeignKey(related_name='created_elcid_travel_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='travel',
            name='update',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='travel',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_elcid_travel_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
