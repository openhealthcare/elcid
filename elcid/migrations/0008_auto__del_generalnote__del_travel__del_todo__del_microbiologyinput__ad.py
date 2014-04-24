# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'GeneralNote'
        db.delete_table(u'elcid_generalnote')

        # Deleting model 'Travel'
        db.delete_table(u'elcid_travel')

        # Deleting model 'Todo'
        db.delete_table(u'elcid_todo')

        # Deleting model 'MicrobiologyInput'
        db.delete_table(u'elcid_microbiologyinput')

        # Adding model 'OPATReview'
        db.create_table(u'elcid_opatreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('rv_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('discussion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opat_plan', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('next_review', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['OPATReview'])

        # Adding model 'OPATOutstandingIssues'
        db.create_table(u'elcid_opatoutstandingissues', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'elcid', ['OPATOutstandingIssues'])

        # Adding model 'Line'
        db.create_table(u'elcid_line', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('line_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('insertion_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('inserted_by', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('removal_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('complications', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('removal_reason', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('special_instructions', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'elcid', ['Line'])

        # Adding model 'AntimicrobialPlan'
        db.create_table(u'elcid_antimicrobialplan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('iv_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('iv_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('oral_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('oral_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['AntimicrobialPlan'])

        # Adding field 'Antimicrobial.delivered_by'
        db.add_column(u'elcid_antimicrobial', 'delivered_by',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Location.opat_referral_route'
        db.add_column(u'elcid_location', 'opat_referral_route',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Location.opat_referral_team'
        db.add_column(u'elcid_location', 'opat_referral_team',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Location.opat_referral'
        db.add_column(u'elcid_location', 'opat_referral',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Location.opat_discharge'
        db.add_column(u'elcid_location', 'opat_discharge',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'GeneralNote'
        db.create_table(u'elcid_generalnote', (
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'elcid', ['GeneralNote'])

        # Adding model 'Travel'
        db.create_table(u'elcid_travel', (
            ('reason_for_travel_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('specific_exposures', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('dates', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('destination_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Destination'], null=True, blank=True)),
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('destination_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reason_for_travel_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Travel_reason'], null=True, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['Travel'])

        # Adding model 'Todo'
        db.create_table(u'elcid_todo', (
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'elcid', ['Todo'])

        # Adding model 'MicrobiologyInput'
        db.create_table(u'elcid_microbiologyinput', (
            ('consistency_token', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('discussed_with', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('change_in_antibiotic_prescription', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agreed_plan', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('referred_to_opat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Episode'], null=True)),
            ('reason_for_interaction_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opal.Clinical_advice_reason_for_interaction'], null=True, blank=True)),
            ('clinical_advice_given', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('infection_control_advice_given', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('clinical_discussion', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('reason_for_interaction_ft', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'elcid', ['MicrobiologyInput'])

        # Deleting model 'OPATReview'
        db.delete_table(u'elcid_opatreview')

        # Deleting model 'OPATOutstandingIssues'
        db.delete_table(u'elcid_opatoutstandingissues')

        # Deleting model 'Line'
        db.delete_table(u'elcid_line')

        # Deleting model 'AntimicrobialPlan'
        db.delete_table(u'elcid_antimicrobialplan')

        # Deleting field 'Antimicrobial.delivered_by'
        db.delete_column(u'elcid_antimicrobial', 'delivered_by')

        # Deleting field 'Location.opat_referral_route'
        db.delete_column(u'elcid_location', 'opat_referral_route')

        # Deleting field 'Location.opat_referral_team'
        db.delete_column(u'elcid_location', 'opat_referral_team')

        # Deleting field 'Location.opat_referral'
        db.delete_column(u'elcid_location', 'opat_referral')

        # Deleting field 'Location.opat_discharge'
        db.delete_column(u'elcid_location', 'opat_discharge')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'elcid.allergies': {
            'Meta': {'object_name': 'Allergies'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'drug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial']", 'null': 'True', 'blank': 'True'}),
            'drug_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"}),
            'provisional': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.antimicrobial': {
            'Meta': {'object_name': 'Antimicrobial'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'delivered_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
        u'elcid.antimicrobialplan': {
            'Meta': {'object_name': 'AntimicrobialPlan'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iv_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'iv_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'oral_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'oral_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.demographics': {
            'Meta': {'object_name': 'Demographics'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'country_of_birth_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Destination']", 'null': 'True', 'blank': 'True'}),
            'country_of_birth_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
        u'elcid.line': {
            'Meta': {'object_name': 'Line'},
            'complications': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inserted_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'insertion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'line_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'removal_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'removal_reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'special_instructions': ('django.db.models.fields.TextField', [], {})
        },
        u'elcid.location': {
            'Meta': {'object_name': 'Location'},
            'bed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'hospital': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opat_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'opat_referral': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'opat_referral_route': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'opat_referral_team': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
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
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
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
        u'elcid.opatoutstandingissues': {
            'Meta': {'object_name': 'OPATOutstandingIssues'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.opatreview': {
            'Meta': {'object_name': 'OPATReview'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'next_review': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'opat_plan': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rv_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.pastmedicalhistory': {
            'Meta': {'object_name': 'PastMedicalHistory'},
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
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
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_admission': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['elcid']