# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'LabTest.vca_igm'
        db.delete_column(u'elcid_labtest', 'vca_igm')

        # Deleting field 'LabTest.parainfluenza'
        db.delete_column(u'elcid_labtest', 'parainfluenza')

        # Deleting field 'LabTest.rpr'
        db.delete_column(u'elcid_labtest', 'rpr')

        # Deleting field 'LabTest.anti_hbs'
        db.delete_column(u'elcid_labtest', 'anti_hbs')

        # Deleting field 'LabTest.rotavirus'
        db.delete_column(u'elcid_labtest', 'rotavirus')

        # Deleting field 'LabTest.norovirus'
        db.delete_column(u'elcid_labtest', 'norovirus')

        # Deleting field 'LabTest.adenovirus'
        db.delete_column(u'elcid_labtest', 'adenovirus')

        # Deleting field 'LabTest.parasitaemia'
        db.delete_column(u'elcid_labtest', 'parasitaemia')

        # Deleting field 'LabTest.metapneumovirus'
        db.delete_column(u'elcid_labtest', 'metapneumovirus')

        # Deleting field 'LabTest.syphilis'
        db.delete_column(u'elcid_labtest', 'syphilis')

        # Deleting field 'LabTest.rsv'
        db.delete_column(u'elcid_labtest', 'rsv')

        # Deleting field 'LabTest.cryptosporidium'
        db.delete_column(u'elcid_labtest', 'cryptosporidium')

        # Deleting field 'LabTest.vca_igg'
        db.delete_column(u'elcid_labtest', 'vca_igg')

        # Deleting field 'LabTest.c_difficile_antigen'
        db.delete_column(u'elcid_labtest', 'c_difficile_antigen')

        # Deleting field 'LabTest.microscopy'
        db.delete_column(u'elcid_labtest', 'microscopy')

        # Deleting field 'LabTest.vzv'
        db.delete_column(u'elcid_labtest', 'vzv')

        # Deleting field 'LabTest.entamoeba_histolytica'
        db.delete_column(u'elcid_labtest', 'entamoeba_histolytica')

        # Deleting field 'LabTest.cmv'
        db.delete_column(u'elcid_labtest', 'cmv')

        # Deleting field 'LabTest.viral_load'
        db.delete_column(u'elcid_labtest', 'viral_load')

        # Deleting field 'LabTest.enterovirus'
        db.delete_column(u'elcid_labtest', 'enterovirus')

        # Deleting field 'LabTest.ebv'
        db.delete_column(u'elcid_labtest', 'ebv')

        # Deleting field 'LabTest.c_difficile_toxin'
        db.delete_column(u'elcid_labtest', 'c_difficile_toxin')

        # Deleting field 'LabTest.giardia'
        db.delete_column(u'elcid_labtest', 'giardia')

        # Deleting field 'LabTest.resistant_antibiotics'
        db.delete_column(u'elcid_labtest', 'resistant_antibiotics')

        # Deleting field 'LabTest.igg'
        db.delete_column(u'elcid_labtest', 'igg')

        # Deleting field 'LabTest.ebna_igg'
        db.delete_column(u'elcid_labtest', 'ebna_igg')

        # Deleting field 'LabTest.anti_hbcore_igm'
        db.delete_column(u'elcid_labtest', 'anti_hbcore_igm')

        # Deleting field 'LabTest.tppa'
        db.delete_column(u'elcid_labtest', 'tppa')

        # Deleting field 'LabTest.igm'
        db.delete_column(u'elcid_labtest', 'igm')

        # Deleting field 'LabTest.anti_hbcore_igg'
        db.delete_column(u'elcid_labtest', 'anti_hbcore_igg')

        # Deleting field 'LabTest.antimicrobial_suceptability_fk'
        db.delete_column(u'elcid_labtest', 'antimicrobial_suceptability_fk_id')

        # Deleting field 'LabTest.hsv'
        db.delete_column(u'elcid_labtest', 'hsv')

        # Deleting field 'LabTest.antimicrobial_suceptability_ft'
        db.delete_column(u'elcid_labtest', 'antimicrobial_suceptability_ft')

        # Deleting field 'LabTest.hbsag'
        db.delete_column(u'elcid_labtest', 'hbsag')

        # Deleting field 'LabTest.influenza_a'
        db.delete_column(u'elcid_labtest', 'influenza_a')

        # Deleting field 'LabTest.influenza_b'
        db.delete_column(u'elcid_labtest', 'influenza_b')

        # Deleting field 'LabTest.species'
        db.delete_column(u'elcid_labtest', 'species')

        # Deleting field 'LabTest.hsv_2'
        db.delete_column(u'elcid_labtest', 'hsv_2')

        # Deleting field 'LabTest.hsv_1'
        db.delete_column(u'elcid_labtest', 'hsv_1')

        # Deleting field 'LabTest.organism'
        db.delete_column(u'elcid_labtest', 'organism')

        # Deleting field 'LabTest.sensitive_antibiotics'
        db.delete_column(u'elcid_labtest', 'sensitive_antibiotics')

        # Adding field 'LabTest.antimicrobial_susceptability_fk'
        db.add_column(u'elcid_labtest', 'antimicrobial_susceptability_fk',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elcid.Antimicrobial_susceptability'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.antimicrobial_susceptability_ft'
        db.add_column(u'elcid_labtest', 'antimicrobial_susceptability_ft',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'LabTest.vca_igm'
        db.add_column(u'elcid_labtest', 'vca_igm',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.parainfluenza'
        db.add_column(u'elcid_labtest', 'parainfluenza',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.rpr'
        db.add_column(u'elcid_labtest', 'rpr',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.anti_hbs'
        db.add_column(u'elcid_labtest', 'anti_hbs',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.rotavirus'
        db.add_column(u'elcid_labtest', 'rotavirus',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.norovirus'
        db.add_column(u'elcid_labtest', 'norovirus',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.adenovirus'
        db.add_column(u'elcid_labtest', 'adenovirus',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.parasitaemia'
        db.add_column(u'elcid_labtest', 'parasitaemia',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.metapneumovirus'
        db.add_column(u'elcid_labtest', 'metapneumovirus',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.syphilis'
        db.add_column(u'elcid_labtest', 'syphilis',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.rsv'
        db.add_column(u'elcid_labtest', 'rsv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.cryptosporidium'
        db.add_column(u'elcid_labtest', 'cryptosporidium',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.vca_igg'
        db.add_column(u'elcid_labtest', 'vca_igg',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.c_difficile_antigen'
        db.add_column(u'elcid_labtest', 'c_difficile_antigen',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.microscopy'
        db.add_column(u'elcid_labtest', 'microscopy',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.vzv'
        db.add_column(u'elcid_labtest', 'vzv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.entamoeba_histolytica'
        db.add_column(u'elcid_labtest', 'entamoeba_histolytica',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.cmv'
        db.add_column(u'elcid_labtest', 'cmv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.viral_load'
        db.add_column(u'elcid_labtest', 'viral_load',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.enterovirus'
        db.add_column(u'elcid_labtest', 'enterovirus',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.ebv'
        db.add_column(u'elcid_labtest', 'ebv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.c_difficile_toxin'
        db.add_column(u'elcid_labtest', 'c_difficile_toxin',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.giardia'
        db.add_column(u'elcid_labtest', 'giardia',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.resistant_antibiotics'
        db.add_column(u'elcid_labtest', 'resistant_antibiotics',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.igg'
        db.add_column(u'elcid_labtest', 'igg',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.ebna_igg'
        db.add_column(u'elcid_labtest', 'ebna_igg',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.anti_hbcore_igm'
        db.add_column(u'elcid_labtest', 'anti_hbcore_igm',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.tppa'
        db.add_column(u'elcid_labtest', 'tppa',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.igm'
        db.add_column(u'elcid_labtest', 'igm',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.anti_hbcore_igg'
        db.add_column(u'elcid_labtest', 'anti_hbcore_igg',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.antimicrobial_suceptability_fk'
        db.add_column(u'elcid_labtest', 'antimicrobial_suceptability_fk',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elcid.Antimicrobial_susceptability'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.hsv'
        db.add_column(u'elcid_labtest', 'hsv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.antimicrobial_suceptability_ft'
        db.add_column(u'elcid_labtest', 'antimicrobial_suceptability_ft',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.hbsag'
        db.add_column(u'elcid_labtest', 'hbsag',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.influenza_a'
        db.add_column(u'elcid_labtest', 'influenza_a',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.influenza_b'
        db.add_column(u'elcid_labtest', 'influenza_b',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.species'
        db.add_column(u'elcid_labtest', 'species',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.hsv_2'
        db.add_column(u'elcid_labtest', 'hsv_2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.hsv_1'
        db.add_column(u'elcid_labtest', 'hsv_1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.organism'
        db.add_column(u'elcid_labtest', 'organism',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'LabTest.sensitive_antibiotics'
        db.add_column(u'elcid_labtest', 'sensitive_antibiotics',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Deleting field 'LabTest.antimicrobial_susceptability_fk'
        db.delete_column(u'elcid_labtest', 'antimicrobial_susceptability_fk_id')

        # Deleting field 'LabTest.antimicrobial_susceptability_ft'
        db.delete_column(u'elcid_labtest', 'antimicrobial_susceptability_ft')


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
            'drug_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"}),
            'provisional': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.antimicrobial': {
            'Meta': {'object_name': 'Antimicrobial'},
            'adverse_event_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_adverse_event']", 'null': 'True', 'blank': 'True'}),
            'adverse_event_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'delivered_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dose': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'drug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial']", 'null': 'True', 'blank': 'True'}),
            'drug_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'frequency_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_frequency']", 'null': 'True', 'blank': 'True'}),
            'frequency_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_route']", 'null': 'True', 'blank': 'True'}),
            'route_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.antimicrobial_susceptability': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial_susceptability'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.appointment': {
            'Meta': {'object_name': 'Appointment'},
            'appointment_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'appointment_with': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.carers': {
            'Meta': {'object_name': 'Carers'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'gp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.GP']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nurse': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.CommunityNurse']", 'null': 'True', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"})
        },
        u'elcid.checkpoints_assay': {
            'Meta': {'ordering': "['name']", 'object_name': 'Checkpoints_assay'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.checkpointsassay': {
            'Meta': {'object_name': 'CheckpointsAssay'},
            'checkpoint': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.contactdetails': {
            'Meta': {'object_name': 'ContactDetails'},
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tel1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.demographics': {
            'Meta': {'object_name': 'Demographics'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'country_of_birth_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Destination']", 'null': 'True', 'blank': 'True'}),
            'country_of_birth_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'hospital_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nhs_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"})
        },
        u'elcid.diagnosis': {
            'Meta': {'object_name': 'Diagnosis'},
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
        u'elcid.labspecimin': {
            'Meta': {'object_name': 'LabSpecimin'},
            'appearance_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Specimin_appearance']", 'null': 'True', 'blank': 'True'}),
            'appearance_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'biobanking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'biobanking_box': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_biobanked': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_collected': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_tested': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'epithelial_cell': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'specimin_type_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Specimin']", 'null': 'True', 'blank': 'True'}),
            'specimin_type_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'volume_biobanked': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'white_blood_cells': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.labtest': {
            'Meta': {'object_name': 'LabTest'},
            'antimicrobial_susceptability_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Antimicrobial_susceptability']", 'null': 'True', 'blank': 'True'}),
            'antimicrobial_susceptability_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'biobanked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'carbapenemase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_ordered': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_retrieved': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'esbl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'freezer_box_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organism_details_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Organism_details']", 'null': 'True', 'blank': 'True'}),
            'organism_details_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'retrieved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'significant_organism': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'elcid.line': {
            'Meta': {'object_name': 'Line'},
            'complications_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_complication']", 'null': 'True', 'blank': 'True'}),
            'complications_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'external_length': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inserted_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'insertion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'insertion_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'line_type_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_type']", 'null': 'True', 'blank': 'True'}),
            'line_type_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'removal_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'removal_reason_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_removal_reason']", 'null': 'True', 'blank': 'True'}),
            'removal_reason_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'removal_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'site_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_site']", 'null': 'True', 'blank': 'True'}),
            'site_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'opat_referral_consultant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'opat_referral_route': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'opat_referral_team': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'opat_referral_team_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'reason_for_interaction_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
        u'elcid.opatlineassessment': {
            'Meta': {'object_name': 'OPATLineAssessment'},
            'assessment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bionector_change_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'dressing_change_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dressing_change_reason': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dressing_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vip_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.opatmeta': {
            'Meta': {'object_name': 'OPATMeta'},
            'cause_of_death': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'death_category': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'deceased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'readmission_cause': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'readmitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reason_for_stopping': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'review_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stopping_iv_details': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'treatment_outcome': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'unplanned_stop_reason_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Unplanned_stop']", 'null': 'True', 'blank': 'True'}),
            'unplanned_stop_reason_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.opatoutstandingissues': {
            'Meta': {'object_name': 'OPATOutstandingIssues'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.opatrejection': {
            'Meta': {'object_name': 'OPATRejection'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decided_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'rv_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.organism_details': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organism_details'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.pastmedicalhistory': {
            'Meta': {'object_name': 'PastMedicalHistory'},
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        u'elcid.presentingcomplaint': {
            'Meta': {'object_name': 'PresentingComplaint'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'duration_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Duration']", 'null': 'True', 'blank': 'True'}),
            'duration_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symptom_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Symptom']", 'null': 'True', 'blank': 'True'}),
            'symptom_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.ridrtitest': {
            'Meta': {'object_name': 'RidRTITest'},
            'absm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ascn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chlamydophila_pneumoniae': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'coronavirus_nl63': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coronavirus_nl63_229e': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coronavirus_oc43': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ctx_m': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'essa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'haemophilus_influenzae': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'influenza_a': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'influenza_b_coronavirus_oc43': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'klebsiella_spp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kpc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legionella_pneumophila': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meca': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mtc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mycoplasma_pneumoniae': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ndm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nocardia_spp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'oxa_48': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pneumocystis_jiroveci': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pseudomonas_aeruginosa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rhodococcus_equi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rsva': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rsvb': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shv_esbl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'staphylococcus_mrsa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'streptococcus_pneumoniae': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tem_esbl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vim': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.specimin': {
            'Meta': {'ordering': "['name']", 'object_name': 'Specimin'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.specimin_appearance': {
            'Meta': {'ordering': "['name']", 'object_name': 'Specimin_appearance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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
            'destination_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason_for_travel_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Travel_reason']", 'null': 'True', 'blank': 'True'}),
            'reason_for_travel_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'specific_exposures': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'elcid.unplanned_stop': {
            'Meta': {'ordering': "['name']", 'object_name': 'Unplanned_stop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.antimicrobial': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.antimicrobial_adverse_event': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial_adverse_event'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.antimicrobial_frequency': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial_frequency'},
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
        u'opal.communitynurse': {
            'Meta': {'object_name': 'CommunityNurse'},
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tel1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
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
        u'opal.duration': {
            'Meta': {'ordering': "['name']", 'object_name': 'Duration'},
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
        u'opal.gp': {
            'Meta': {'object_name': 'GP'},
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tel1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'opal.line_complication': {
            'Meta': {'ordering': "['name']", 'object_name': 'Line_complication'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.line_removal_reason': {
            'Meta': {'ordering': "['name']", 'object_name': 'Line_removal_reason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.line_site': {
            'Meta': {'ordering': "['name']", 'object_name': 'Line_site'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.line_type': {
            'Meta': {'ordering': "['name']", 'object_name': 'Line_type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.patient': {
            'Meta': {'object_name': 'Patient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'opal.symptom': {
            'Meta': {'ordering': "['name']", 'object_name': 'Symptom'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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