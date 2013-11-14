# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Demographics'
        db.create_table(u'elcid_demographics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Patient'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('hospital_number', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['Demographics'])

        # Adding model 'Location'
        db.create_table(u'elcid_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('hospital', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('ward', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('bed', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('date_of_admission', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('discharge_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['Location'])

        # Adding model 'Diagnosis'
        db.create_table(u'elcid_diagnosis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('provisional', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('date_of_diagnosis', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('condition_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Condition'], null=True, blank=True)),
            ('condition_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['Diagnosis'])

        # Adding model 'PastMedicalHistory'
        db.create_table(u'elcid_pastmedicalhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('condition_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Condition'], null=True, blank=True)),
            ('condition_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['PastMedicalHistory'])

        # Adding model 'GeneralNote'
        db.create_table(u'elcid_generalnote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'elcid', ['GeneralNote'])

        # Adding model 'Travel'
        db.create_table(u'elcid_travel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('dates', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('specific_exposures', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('destination_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Destination'], null=True, blank=True)),
            ('destination_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('reason_for_travel_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Travel_reason'], null=True, blank=True)),
            ('reason_for_travel_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['Travel'])

        # Adding model 'Antimicrobial'
        db.create_table(u'elcid_antimicrobial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('dose', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('route_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Antimicrobial_route'], null=True, blank=True)),
            ('route_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('drug_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Antimicrobial'], null=True, blank=True)),
            ('drug_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['Antimicrobial'])

        # Adding model 'MicrobiologyInput'
        db.create_table(u'elcid_microbiologyinput', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('clinical_discussion', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('agreed_plan', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('discussed_with', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('clinical_advice_given', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('infection_control_advice_given', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('change_in_antibiotic_prescription', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('referred_to_opat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reason_for_interaction_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Clinical_advice_reason_for_interaction'], null=True, blank=True)),
            ('reason_for_interaction_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['MicrobiologyInput'])

        # Adding model 'Todo'
        db.create_table(u'elcid_todo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'elcid', ['Todo'])

        # Adding model 'MicrobiologyTest'
        db.create_table(u'elcid_microbiologytest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('test', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_ordered', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('microscopy', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('organism', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('sensitive_antibiotics', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('resistant_antibiotics', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('igm', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('igg', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('vca_igm', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('vca_igg', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('ebna_igg', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('hbsag', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('anti_hbs', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('anti_hbcore_igm', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('anti_hbcore_igg', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('rpr', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('tppa', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('viral_load', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('parasitaemia', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('hsv', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('vzv', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('syphilis', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('c_difficile_antigen', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('c_difficile_toxin', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('hsv_1', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('hsv_2', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('enterovirus', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('cmv', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('ebv', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('influenza_a', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('influenza_b', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('parainfluenza', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('metapneumovirus', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('rsv', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('adenovirus', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('norovirus', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('rotavirus', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('giardia', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('entamoeba_histolytica', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('cryptosporidium', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['MicrobiologyTest'])


    def backwards(self, orm):
        # Deleting model 'Demographics'
        db.delete_table(u'elcid_demographics')

        # Deleting model 'Location'
        db.delete_table(u'elcid_location')

        # Deleting model 'Diagnosis'
        db.delete_table(u'elcid_diagnosis')

        # Deleting model 'PastMedicalHistory'
        db.delete_table(u'elcid_pastmedicalhistory')

        # Deleting model 'GeneralNote'
        db.delete_table(u'elcid_generalnote')

        # Deleting model 'Travel'
        db.delete_table(u'elcid_travel')

        # Deleting model 'Antimicrobial'
        db.delete_table(u'elcid_antimicrobial')

        # Deleting model 'MicrobiologyInput'
        db.delete_table(u'elcid_microbiologyinput')

        # Deleting model 'Todo'
        db.delete_table(u'elcid_todo')

        # Deleting model 'MicrobiologyTest'
        db.delete_table(u'elcid_microbiologytest')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'elcid.antimicrobial': {
            'Meta': {'object_name': 'Antimicrobial'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'dose': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'drug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial']", 'null': 'True', 'blank': 'True'}),
            'drug_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_route']", 'null': 'True', 'blank': 'True'}),
            'route_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.demographics': {
            'Meta': {'object_name': 'Demographics'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hospital_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"})
        },
        u'elcid.diagnosis': {
            'Meta': {'object_name': 'Diagnosis'},
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_diagnosis': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provisional': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.generalnote': {
            'Meta': {'object_name': 'GeneralNote'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.location': {
            'Meta': {'object_name': 'Location'},
            'bed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_admission': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'hospital': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'elcid.microbiologyinput': {
            'Meta': {'object_name': 'MicrobiologyInput'},
            'agreed_plan': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'change_in_antibiotic_prescription': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clinical_advice_given': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clinical_discussion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'discussed_with': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_control_advice_given': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'reason_for_interaction_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Clinical_advice_reason_for_interaction']", 'null': 'True', 'blank': 'True'}),
            'reason_for_interaction_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'referred_to_opat': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.microbiologytest': {
            'Meta': {'object_name': 'MicrobiologyTest'},
            'adenovirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'anti_hbcore_igg': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'anti_hbcore_igm': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'anti_hbs': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'c_difficile_antigen': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'c_difficile_toxin': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'cmv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'cryptosporidium': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'date_ordered': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ebna_igg': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'ebv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'entamoeba_histolytica': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'enterovirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'giardia': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hbsag': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hsv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hsv_1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hsv_2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'igg': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'igm': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'influenza_a': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'influenza_b': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'metapneumovirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'microscopy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'norovirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'organism': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'parainfluenza': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'parasitaemia': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'resistant_antibiotics': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'rotavirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'rpr': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'rsv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'sensitive_antibiotics': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'syphilis': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tppa': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'vca_igg': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'vca_igm': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'viral_load': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'vzv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'elcid.pastmedicalhistory': {
            'Meta': {'object_name': 'PastMedicalHistory'},
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        u'elcid.todo': {
            'Meta': {'object_name': 'Todo'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.travel': {
            'Meta': {'object_name': 'Travel'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'dates': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'destination_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Destination']", 'null': 'True', 'blank': 'True'}),
            'destination_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason_for_travel_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Travel_reason']", 'null': 'True', 'blank': 'True'}),
            'reason_for_travel_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'specific_exposures': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'opal.antimicrobial': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.antimicrobial_route': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial_route'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.clinical_advice_reason_for_interaction': {
            'Meta': {'ordering': "['name']", 'object_name': 'Clinical_advice_reason_for_interaction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.condition': {
            'Meta': {'ordering': "['name']", 'object_name': 'Condition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.destination': {
            'Meta': {'ordering': "['name']", 'object_name': 'Destination'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.episode': {
            'Meta': {'object_name': 'Episode'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"})
        },
        u'opal.patient': {
            'Meta': {'object_name': 'Patient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'opal.synonym': {
            'Meta': {'unique_together': "(('name', 'content_type'),)", 'object_name': 'Synonym'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'opal.travel_reason': {
            'Meta': {'ordering': "['name']", 'object_name': 'Travel_reason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['elcid']