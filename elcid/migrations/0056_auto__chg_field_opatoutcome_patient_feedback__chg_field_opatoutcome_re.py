# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'OPATOutcome.patient_feedback'
        db.alter_column(u'elcid_opatoutcome', 'patient_feedback', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATOutcome.readmitted'
        db.alter_column(u'elcid_opatoutcome', 'readmitted', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATOutcome.deceased'
        db.alter_column(u'elcid_opatoutcome', 'deceased', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.acinetobacter_baumannii'
        db.alter_column(u'elcid_ridrtitest', 'acinetobacter_baumannii', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.cap_coronavirus_oc43'
        db.alter_column(u'elcid_ridrtitest', 'cap_coronavirus_oc43', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.haemophilus_influenzae'
        db.alter_column(u'elcid_ridrtitest', 'haemophilus_influenzae', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.cap_coronavirus_229e'
        db.alter_column(u'elcid_ridrtitest', 'cap_coronavirus_229e', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.legionella_pneumophila'
        db.alter_column(u'elcid_ridrtitest', 'legionella_pneumophila', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.mycoplasma_pneumoniae'
        db.alter_column(u'elcid_ridrtitest', 'mycoplasma_pneumoniae', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.vim'
        db.alter_column(u'elcid_ridrtitest', 'vim', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.tem_esbl'
        db.alter_column(u'elcid_ridrtitest', 'tem_esbl', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.shv_esbl'
        db.alter_column(u'elcid_ridrtitest', 'shv_esbl', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.orti_coronavirus_nl63'
        db.alter_column(u'elcid_ridrtitest', 'orti_coronavirus_nl63', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.staphylococcus_aureus'
        db.alter_column(u'elcid_ridrtitest', 'staphylococcus_aureus', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.ctx_m'
        db.alter_column(u'elcid_ridrtitest', 'ctx_m', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.rhodococcus_equi'
        db.alter_column(u'elcid_ridrtitest', 'rhodococcus_equi', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.staphylococcus_mrsa'
        db.alter_column(u'elcid_ridrtitest', 'staphylococcus_mrsa', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.orti_coronavirus_hku1'
        db.alter_column(u'elcid_ridrtitest', 'orti_coronavirus_hku1', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.rsvb'
        db.alter_column(u'elcid_ridrtitest', 'rsvb', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.rsva'
        db.alter_column(u'elcid_ridrtitest', 'rsva', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.oxa_48'
        db.alter_column(u'elcid_ridrtitest', 'oxa_48', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.imp'
        db.alter_column(u'elcid_ridrtitest', 'imp', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.chlamydophila_pneumoniae'
        db.alter_column(u'elcid_ridrtitest', 'chlamydophila_pneumoniae', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.streptococcus_pneumoniae'
        db.alter_column(u'elcid_ridrtitest', 'streptococcus_pneumoniae', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.cap_coronavirus_nl63'
        db.alter_column(u'elcid_ridrtitest', 'cap_coronavirus_nl63', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.senotophomonas_maltophilia'
        db.alter_column(u'elcid_ridrtitest', 'senotophomonas_maltophilia', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.orti_coronavirus_oc43'
        db.alter_column(u'elcid_ridrtitest', 'orti_coronavirus_oc43', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.aspergillus_spp'
        db.alter_column(u'elcid_ridrtitest', 'aspergillus_spp', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.orti_coronavirus_229e'
        db.alter_column(u'elcid_ridrtitest', 'orti_coronavirus_229e', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.ndm'
        db.alter_column(u'elcid_ridrtitest', 'ndm', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.nocardia_spp'
        db.alter_column(u'elcid_ridrtitest', 'nocardia_spp', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.pneumocystis_jiroveci'
        db.alter_column(u'elcid_ridrtitest', 'pneumocystis_jiroveci', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.enterobacter_spp'
        db.alter_column(u'elcid_ridrtitest', 'enterobacter_spp', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.influenza_a'
        db.alter_column(u'elcid_ridrtitest', 'influenza_a', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.influenza_b'
        db.alter_column(u'elcid_ridrtitest', 'influenza_b', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.pseudomonas_aeruginosa'
        db.alter_column(u'elcid_ridrtitest', 'pseudomonas_aeruginosa', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.cap_coronavirus_hku1'
        db.alter_column(u'elcid_ridrtitest', 'cap_coronavirus_hku1', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.kpc'
        db.alter_column(u'elcid_ridrtitest', 'kpc', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.cryptococcus_neoformans'
        db.alter_column(u'elcid_ridrtitest', 'cryptococcus_neoformans', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.mtc'
        db.alter_column(u'elcid_ridrtitest', 'mtc', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.meca'
        db.alter_column(u'elcid_ridrtitest', 'meca', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'RidRTITest.klebsiella_spp'
        db.alter_column(u'elcid_ridrtitest', 'klebsiella_spp', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATMeta.readmitted'
        db.alter_column(u'elcid_opatmeta', 'readmitted', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATMeta.deceased'
        db.alter_column(u'elcid_opatmeta', 'deceased', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATLineAssessment.lumen_flush_ok'
        db.alter_column(u'elcid_opatlineassessment', 'lumen_flush_ok', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATLineAssessment.cm_from_exit_site'
        db.alter_column(u'elcid_opatlineassessment', 'cm_from_exit_site', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATLineAssessment.dressing_intact'
        db.alter_column(u'elcid_opatlineassessment', 'dressing_intact', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATLineAssessment.blood_drawback_seen'
        db.alter_column(u'elcid_opatlineassessment', 'blood_drawback_seen', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'PrimaryDiagnosis.confirmed'
        db.alter_column(u'elcid_primarydiagnosis', 'confirmed', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'LabTest.significant_organism'
        db.alter_column(u'elcid_labtest', 'significant_organism', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'LabTest.organism_biobanked'
        db.alter_column(u'elcid_labtest', 'organism_biobanked', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'LabTest.carbapenemase'
        db.alter_column(u'elcid_labtest', 'carbapenemase', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'LabTest.retrieved'
        db.alter_column(u'elcid_labtest', 'retrieved', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'LabTest.esbl'
        db.alter_column(u'elcid_labtest', 'esbl', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'LabTest.sweep_biobanked'
        db.alter_column(u'elcid_labtest', 'sweep_biobanked', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ctx_m_8_25_group'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_8_25_group', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.shv_wt'
        db.alter_column(u'elcid_checkpointsassay', 'shv_wt', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.tem_wt'
        db.alter_column(u'elcid_checkpointsassay', 'tem_wt', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.vim'
        db.alter_column(u'elcid_checkpointsassay', 'vim', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.dha'
        db.alter_column(u'elcid_checkpointsassay', 'dha', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ctx_m_2_group'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_2_group', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.oxa_48_like'
        db.alter_column(u'elcid_checkpointsassay', 'oxa_48_like', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.shv_g238a'
        db.alter_column(u'elcid_checkpointsassay', 'shv_g238a', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ctx_m_1_like'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_1_like', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ctx_m_32_like'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_32_like', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.fox'
        db.alter_column(u'elcid_checkpointsassay', 'fox', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.negative'
        db.alter_column(u'elcid_checkpointsassay', 'negative', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.per'
        db.alter_column(u'elcid_checkpointsassay', 'per', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.imp'
        db.alter_column(u'elcid_checkpointsassay', 'imp', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ctx_m_1_group'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_1_group', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ctx_m_15_like'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_15_like', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.shv_g238s'
        db.alter_column(u'elcid_checkpointsassay', 'shv_g238s', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.cmy_i_mox'
        db.alter_column(u'elcid_checkpointsassay', 'cmy_i_mox', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.veb'
        db.alter_column(u'elcid_checkpointsassay', 'veb', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ctx_m_9_group'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_9_group', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.tem_g238s'
        db.alter_column(u'elcid_checkpointsassay', 'tem_g238s', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ges'
        db.alter_column(u'elcid_checkpointsassay', 'ges', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.tem_r164h'
        db.alter_column(u'elcid_checkpointsassay', 'tem_r164h', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.tem_e104k'
        db.alter_column(u'elcid_checkpointsassay', 'tem_e104k', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.oxa_24_like'
        db.alter_column(u'elcid_checkpointsassay', 'oxa_24_like', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ctx_m_3_like'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_3_like', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.tem_r164c'
        db.alter_column(u'elcid_checkpointsassay', 'tem_r164c', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.cmy_ii'
        db.alter_column(u'elcid_checkpointsassay', 'cmy_ii', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.shv_e240k'
        db.alter_column(u'elcid_checkpointsassay', 'shv_e240k', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.tem_r164s'
        db.alter_column(u'elcid_checkpointsassay', 'tem_r164s', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.act_mir'
        db.alter_column(u'elcid_checkpointsassay', 'act_mir', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.gim'
        db.alter_column(u'elcid_checkpointsassay', 'gim', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.acc'
        db.alter_column(u'elcid_checkpointsassay', 'acc', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.ndm'
        db.alter_column(u'elcid_checkpointsassay', 'ndm', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.bel'
        db.alter_column(u'elcid_checkpointsassay', 'bel', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.oxa_58_like'
        db.alter_column(u'elcid_checkpointsassay', 'oxa_58_like', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.kpc'
        db.alter_column(u'elcid_checkpointsassay', 'kpc', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.oxa_23_like'
        db.alter_column(u'elcid_checkpointsassay', 'oxa_23_like', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'CheckpointsAssay.spm'
        db.alter_column(u'elcid_checkpointsassay', 'spm', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Diagnosis.provisional'
        db.alter_column(u'elcid_diagnosis', 'provisional', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'SecondaryDiagnosis.co_primary'
        db.alter_column(u'elcid_secondarydiagnosis', 'co_primary', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATReview.bung_changed'
        db.alter_column(u'elcid_opatreview', 'bung_changed', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATReview.dressing_changed'
        db.alter_column(u'elcid_opatreview', 'dressing_changed', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'LabSpecimin.biobanking'
        db.alter_column(u'elcid_labspecimin', 'biobanking', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATRejection.oral_available'
        db.alter_column(u'elcid_opatrejection', 'oral_available', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATRejection.patient_suitability'
        db.alter_column(u'elcid_opatrejection', 'patient_suitability', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATRejection.not_fit_for_discharge'
        db.alter_column(u'elcid_opatrejection', 'not_fit_for_discharge', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATRejection.no_social_support'
        db.alter_column(u'elcid_opatrejection', 'no_social_support', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATRejection.not_needed'
        db.alter_column(u'elcid_opatrejection', 'not_needed', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATRejection.patient_choice'
        db.alter_column(u'elcid_opatrejection', 'patient_choice', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'OPATRejection.non_complex_infection'
        db.alter_column(u'elcid_opatrejection', 'non_complex_infection', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Allergies.provisional'
        db.alter_column(u'elcid_allergies', 'provisional', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Travel.malaria_prophylaxis'
        db.alter_column(u'elcid_travel', 'malaria_prophylaxis', self.gf('django.db.models.fields.NullBooleanField')(null=True))

    def backwards(self, orm):

        # Changing field 'OPATOutcome.patient_feedback'
        db.alter_column(u'elcid_opatoutcome', 'patient_feedback', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATOutcome.readmitted'
        db.alter_column(u'elcid_opatoutcome', 'readmitted', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATOutcome.deceased'
        db.alter_column(u'elcid_opatoutcome', 'deceased', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.acinetobacter_baumannii'
        db.alter_column(u'elcid_ridrtitest', 'acinetobacter_baumannii', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.cap_coronavirus_oc43'
        db.alter_column(u'elcid_ridrtitest', 'cap_coronavirus_oc43', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.haemophilus_influenzae'
        db.alter_column(u'elcid_ridrtitest', 'haemophilus_influenzae', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.cap_coronavirus_229e'
        db.alter_column(u'elcid_ridrtitest', 'cap_coronavirus_229e', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.legionella_pneumophila'
        db.alter_column(u'elcid_ridrtitest', 'legionella_pneumophila', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.mycoplasma_pneumoniae'
        db.alter_column(u'elcid_ridrtitest', 'mycoplasma_pneumoniae', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.vim'
        db.alter_column(u'elcid_ridrtitest', 'vim', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.tem_esbl'
        db.alter_column(u'elcid_ridrtitest', 'tem_esbl', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.shv_esbl'
        db.alter_column(u'elcid_ridrtitest', 'shv_esbl', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.orti_coronavirus_nl63'
        db.alter_column(u'elcid_ridrtitest', 'orti_coronavirus_nl63', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.staphylococcus_aureus'
        db.alter_column(u'elcid_ridrtitest', 'staphylococcus_aureus', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.ctx_m'
        db.alter_column(u'elcid_ridrtitest', 'ctx_m', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.rhodococcus_equi'
        db.alter_column(u'elcid_ridrtitest', 'rhodococcus_equi', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.staphylococcus_mrsa'
        db.alter_column(u'elcid_ridrtitest', 'staphylococcus_mrsa', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.orti_coronavirus_hku1'
        db.alter_column(u'elcid_ridrtitest', 'orti_coronavirus_hku1', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.rsvb'
        db.alter_column(u'elcid_ridrtitest', 'rsvb', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.rsva'
        db.alter_column(u'elcid_ridrtitest', 'rsva', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.oxa_48'
        db.alter_column(u'elcid_ridrtitest', 'oxa_48', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.imp'
        db.alter_column(u'elcid_ridrtitest', 'imp', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.chlamydophila_pneumoniae'
        db.alter_column(u'elcid_ridrtitest', 'chlamydophila_pneumoniae', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.streptococcus_pneumoniae'
        db.alter_column(u'elcid_ridrtitest', 'streptococcus_pneumoniae', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.cap_coronavirus_nl63'
        db.alter_column(u'elcid_ridrtitest', 'cap_coronavirus_nl63', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.senotophomonas_maltophilia'
        db.alter_column(u'elcid_ridrtitest', 'senotophomonas_maltophilia', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.orti_coronavirus_oc43'
        db.alter_column(u'elcid_ridrtitest', 'orti_coronavirus_oc43', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.aspergillus_spp'
        db.alter_column(u'elcid_ridrtitest', 'aspergillus_spp', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.orti_coronavirus_229e'
        db.alter_column(u'elcid_ridrtitest', 'orti_coronavirus_229e', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.ndm'
        db.alter_column(u'elcid_ridrtitest', 'ndm', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.nocardia_spp'
        db.alter_column(u'elcid_ridrtitest', 'nocardia_spp', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.pneumocystis_jiroveci'
        db.alter_column(u'elcid_ridrtitest', 'pneumocystis_jiroveci', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.enterobacter_spp'
        db.alter_column(u'elcid_ridrtitest', 'enterobacter_spp', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.influenza_a'
        db.alter_column(u'elcid_ridrtitest', 'influenza_a', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.influenza_b'
        db.alter_column(u'elcid_ridrtitest', 'influenza_b', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.pseudomonas_aeruginosa'
        db.alter_column(u'elcid_ridrtitest', 'pseudomonas_aeruginosa', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.cap_coronavirus_hku1'
        db.alter_column(u'elcid_ridrtitest', 'cap_coronavirus_hku1', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.kpc'
        db.alter_column(u'elcid_ridrtitest', 'kpc', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.cryptococcus_neoformans'
        db.alter_column(u'elcid_ridrtitest', 'cryptococcus_neoformans', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.mtc'
        db.alter_column(u'elcid_ridrtitest', 'mtc', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.meca'
        db.alter_column(u'elcid_ridrtitest', 'meca', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'RidRTITest.klebsiella_spp'
        db.alter_column(u'elcid_ridrtitest', 'klebsiella_spp', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATMeta.readmitted'
        db.alter_column(u'elcid_opatmeta', 'readmitted', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATMeta.deceased'
        db.alter_column(u'elcid_opatmeta', 'deceased', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATLineAssessment.lumen_flush_ok'
        db.alter_column(u'elcid_opatlineassessment', 'lumen_flush_ok', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATLineAssessment.cm_from_exit_site'
        db.alter_column(u'elcid_opatlineassessment', 'cm_from_exit_site', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATLineAssessment.dressing_intact'
        db.alter_column(u'elcid_opatlineassessment', 'dressing_intact', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATLineAssessment.blood_drawback_seen'
        db.alter_column(u'elcid_opatlineassessment', 'blood_drawback_seen', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'PrimaryDiagnosis.confirmed'
        db.alter_column(u'elcid_primarydiagnosis', 'confirmed', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LabTest.significant_organism'
        db.alter_column(u'elcid_labtest', 'significant_organism', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LabTest.organism_biobanked'
        db.alter_column(u'elcid_labtest', 'organism_biobanked', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LabTest.carbapenemase'
        db.alter_column(u'elcid_labtest', 'carbapenemase', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LabTest.retrieved'
        db.alter_column(u'elcid_labtest', 'retrieved', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LabTest.esbl'
        db.alter_column(u'elcid_labtest', 'esbl', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LabTest.sweep_biobanked'
        db.alter_column(u'elcid_labtest', 'sweep_biobanked', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ctx_m_8_25_group'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_8_25_group', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.shv_wt'
        db.alter_column(u'elcid_checkpointsassay', 'shv_wt', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.tem_wt'
        db.alter_column(u'elcid_checkpointsassay', 'tem_wt', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.vim'
        db.alter_column(u'elcid_checkpointsassay', 'vim', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.dha'
        db.alter_column(u'elcid_checkpointsassay', 'dha', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ctx_m_2_group'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_2_group', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.oxa_48_like'
        db.alter_column(u'elcid_checkpointsassay', 'oxa_48_like', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.shv_g238a'
        db.alter_column(u'elcid_checkpointsassay', 'shv_g238a', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ctx_m_1_like'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_1_like', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ctx_m_32_like'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_32_like', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.fox'
        db.alter_column(u'elcid_checkpointsassay', 'fox', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.negative'
        db.alter_column(u'elcid_checkpointsassay', 'negative', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.per'
        db.alter_column(u'elcid_checkpointsassay', 'per', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.imp'
        db.alter_column(u'elcid_checkpointsassay', 'imp', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ctx_m_1_group'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_1_group', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ctx_m_15_like'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_15_like', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.shv_g238s'
        db.alter_column(u'elcid_checkpointsassay', 'shv_g238s', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.cmy_i_mox'
        db.alter_column(u'elcid_checkpointsassay', 'cmy_i_mox', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.veb'
        db.alter_column(u'elcid_checkpointsassay', 'veb', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ctx_m_9_group'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_9_group', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.tem_g238s'
        db.alter_column(u'elcid_checkpointsassay', 'tem_g238s', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ges'
        db.alter_column(u'elcid_checkpointsassay', 'ges', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.tem_r164h'
        db.alter_column(u'elcid_checkpointsassay', 'tem_r164h', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.tem_e104k'
        db.alter_column(u'elcid_checkpointsassay', 'tem_e104k', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.oxa_24_like'
        db.alter_column(u'elcid_checkpointsassay', 'oxa_24_like', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ctx_m_3_like'
        db.alter_column(u'elcid_checkpointsassay', 'ctx_m_3_like', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.tem_r164c'
        db.alter_column(u'elcid_checkpointsassay', 'tem_r164c', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.cmy_ii'
        db.alter_column(u'elcid_checkpointsassay', 'cmy_ii', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.shv_e240k'
        db.alter_column(u'elcid_checkpointsassay', 'shv_e240k', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.tem_r164s'
        db.alter_column(u'elcid_checkpointsassay', 'tem_r164s', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.act_mir'
        db.alter_column(u'elcid_checkpointsassay', 'act_mir', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.gim'
        db.alter_column(u'elcid_checkpointsassay', 'gim', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.acc'
        db.alter_column(u'elcid_checkpointsassay', 'acc', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.ndm'
        db.alter_column(u'elcid_checkpointsassay', 'ndm', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.bel'
        db.alter_column(u'elcid_checkpointsassay', 'bel', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.oxa_58_like'
        db.alter_column(u'elcid_checkpointsassay', 'oxa_58_like', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.kpc'
        db.alter_column(u'elcid_checkpointsassay', 'kpc', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.oxa_23_like'
        db.alter_column(u'elcid_checkpointsassay', 'oxa_23_like', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CheckpointsAssay.spm'
        db.alter_column(u'elcid_checkpointsassay', 'spm', self.gf('django.db.models.fields.BooleanField')())

        # User chose to not deal with backwards NULL issues for 'Diagnosis.provisional'
        raise RuntimeError("Cannot reverse this migration. 'Diagnosis.provisional' and its values cannot be restored.")

        # Changing field 'SecondaryDiagnosis.co_primary'
        db.alter_column(u'elcid_secondarydiagnosis', 'co_primary', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATReview.bung_changed'
        db.alter_column(u'elcid_opatreview', 'bung_changed', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATReview.dressing_changed'
        db.alter_column(u'elcid_opatreview', 'dressing_changed', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LabSpecimin.biobanking'
        db.alter_column(u'elcid_labspecimin', 'biobanking', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATRejection.oral_available'
        db.alter_column(u'elcid_opatrejection', 'oral_available', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATRejection.patient_suitability'
        db.alter_column(u'elcid_opatrejection', 'patient_suitability', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATRejection.not_fit_for_discharge'
        db.alter_column(u'elcid_opatrejection', 'not_fit_for_discharge', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATRejection.no_social_support'
        db.alter_column(u'elcid_opatrejection', 'no_social_support', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATRejection.not_needed'
        db.alter_column(u'elcid_opatrejection', 'not_needed', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATRejection.patient_choice'
        db.alter_column(u'elcid_opatrejection', 'patient_choice', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'OPATRejection.non_complex_infection'
        db.alter_column(u'elcid_opatrejection', 'non_complex_infection', self.gf('django.db.models.fields.BooleanField')())

        # User chose to not deal with backwards NULL issues for 'Allergies.provisional'
        raise RuntimeError("Cannot reverse this migration. 'Allergies.provisional' and its values cannot be restored.")

        # Changing field 'Travel.malaria_prophylaxis'
        db.alter_column(u'elcid_travel', 'malaria_prophylaxis', self.gf('django.db.models.fields.BooleanField')())

    models = {
        u'elcid.allergies': {
            'Meta': {'object_name': 'Allergies'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'drug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial']", 'null': 'True', 'blank': 'True'}),
            'drug_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"}),
            'provisional': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.antimicrobial': {
            'Meta': {'object_name': 'Antimicrobial'},
            'adverse_event_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_adverse_event']", 'null': 'True', 'blank': 'True'}),
            'adverse_event_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'delivered_by_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Drug_delivered']", 'null': 'True', 'blank': 'True'}),
            'delivered_by_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dose': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'drug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial']", 'null': 'True', 'blank': 'True'}),
            'drug_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            'frequency_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_frequency']", 'null': 'True', 'blank': 'True'}),
            'frequency_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason_for_stopping_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Iv_stop']", 'null': 'True', 'blank': 'True'}),
            'reason_for_stopping_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
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
            'acc': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'act_mir': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'bel': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'cmy_i_mox': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'cmy_ii': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'ctx_m_15_like': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ctx_m_1_group': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ctx_m_1_like': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ctx_m_2_group': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ctx_m_32_like': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ctx_m_3_like': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ctx_m_8_25_group': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ctx_m_9_group': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'dha': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            'fox': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ges': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'gim': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'kpc': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ndm': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'negative': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'oxa_23_like': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'oxa_24_like': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'oxa_48_like': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'oxa_58_like': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'per': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'shv_e240k': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'shv_g238a': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'shv_g238s': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'shv_wt': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'spm': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tem_e104k': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tem_g238s': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tem_r164c': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tem_r164h': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tem_r164s': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tem_wt': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'veb': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'vim': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
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
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provisional': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.drug_delivered': {
            'Meta': {'ordering': "['name']", 'object_name': 'Drug_delivered'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.generalnote': {
            'Meta': {'object_name': 'GeneralNote'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.hiv_no': {
            'Meta': {'ordering': "['name']", 'object_name': 'Hiv_no'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.iv_stop': {
            'Meta': {'ordering': "['name']", 'object_name': 'Iv_stop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.labspecimin': {
            'Meta': {'object_name': 'LabSpecimin'},
            'appearance_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Specimin_appearance']", 'null': 'True', 'blank': 'True'}),
            'appearance_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'biobanking': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'biobanking_box': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_biobanked': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_collected': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_tested': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
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
            'antimicrobials_intermediate_fk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'intermediate'", 'null': 'True', 'to': u"orm['elcid.Antimicrobial_susceptability']"}),
            'antimicrobials_intermediate_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'antimicrobials_resistant_fk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'resistant'", 'null': 'True', 'to': u"orm['elcid.Antimicrobial_susceptability']"}),
            'antimicrobials_resistant_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'antimicrobials_susceptible_fk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'susceptible'", 'null': 'True', 'to': u"orm['elcid.Antimicrobial_susceptability']"}),
            'antimicrobials_susceptible_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'carbapenemase': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_ordered': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_retrieved': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            'esbl': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'freezer_box_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organism_biobanked': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'organism_details_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Organism_details']", 'null': 'True', 'blank': 'True'}),
            'organism_details_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'retrieved': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'significant_organism': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'sweep_biobanked': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'elcid.line': {
            'Meta': {'object_name': 'Line'},
            'complications_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_complication']", 'null': 'True', 'blank': 'True'}),
            'complications_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            'external_length': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inserted_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'insertion_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'line_type_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_type']", 'null': 'True', 'blank': 'True'}),
            'line_type_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'removal_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'removal_reason_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_removal_reason']", 'null': 'True', 'blank': 'True'}),
            'removal_reason_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'site_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_site']", 'null': 'True', 'blank': 'True'}),
            'site_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'special_instructions': ('django.db.models.fields.TextField', [], {})
        },
        u'elcid.location': {
            'Meta': {'object_name': 'Location'},
            'bed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
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
            'change_in_antibiotic_prescription': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'clinical_advice_given': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'clinical_discussion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'discussed_with': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_control_advice_given': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'reason_for_interaction_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Clinical_advice_reason_for_interaction']", 'null': 'True', 'blank': 'True'}),
            'reason_for_interaction_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'referred_to_opat': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
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
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            'giardia': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hbsag': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hiv_declined_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Hiv_no']", 'null': 'True', 'blank': 'True'}),
            'hiv_declined_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
        u'elcid.opat_rvt': {
            'Meta': {'ordering': "['name']", 'object_name': 'Opat_rvt'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.opatlineassessment': {
            'Meta': {'object_name': 'OPATLineAssessment'},
            'assessment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bionector_change_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'blood_drawback_seen': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'cm_from_exit_site': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'dressing_change_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dressing_change_reason': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dressing_intact': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'dressing_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lumen_flush_ok': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'vip_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.opatmeta': {
            'Meta': {'object_name': 'OPATMeta'},
            'cause_of_death': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'death_category': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'deceased': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'readmission_cause': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'readmitted': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'reason_for_stopping': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'review_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stopping_iv_details': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'treatment_outcome': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'unplanned_stop_reason_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Unplanned_stop']", 'null': 'True', 'blank': 'True'}),
            'unplanned_stop_reason_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.opatoutcome': {
            'Meta': {'object_name': 'OPATOutcome'},
            'cause_of_death': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'death_category': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'deceased': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'patient_feedback': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'readmission_cause': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'readmitted': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'treatment_outcome': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.opatoutstandingissues': {
            'Meta': {'object_name': 'OPATOutstandingIssues'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.opatrejection': {
            'Meta': {'object_name': 'OPATRejection'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decided_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_social_support': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'non_complex_infection': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'not_fit_for_discharge': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'not_needed': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'oral_available': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'patient_choice': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'patient_suitability': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.opatreview': {
            'Meta': {'object_name': 'OPATReview'},
            'adverse_events_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_adverse_event']", 'null': 'True', 'blank': 'True'}),
            'adverse_events_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bung_changed': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dressing_changed': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'medication_administered': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'next_review': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'opat_plan': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rv_type_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Opat_rvt']", 'null': 'True', 'blank': 'True'}),
            'rv_type_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        u'elcid.presentingcomplaint': {
            'Meta': {'object_name': 'PresentingComplaint'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symptom_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Symptom']", 'null': 'True', 'blank': 'True'}),
            'symptom_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.primarydiagnosis': {
            'Meta': {'object_name': 'PrimaryDiagnosis'},
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.ridrtitest': {
            'Meta': {'object_name': 'RidRTITest'},
            'acinetobacter_baumannii': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'aspergillus_spp': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'cap_coronavirus_229e': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'cap_coronavirus_hku1': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'cap_coronavirus_nl63': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'cap_coronavirus_oc43': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'chlamydophila_pneumoniae': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'cryptococcus_neoformans': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ctx_m': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'enterobacter_spp': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            'haemophilus_influenzae': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'influenza_a': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'influenza_b': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'klebsiella_spp': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'kpc': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'legionella_pneumophila': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'meca': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'mtc': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'mycoplasma_pneumoniae': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ndm': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'nocardia_spp': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'orti_coronavirus_229e': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'orti_coronavirus_hku1': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'orti_coronavirus_nl63': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'orti_coronavirus_oc43': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'oxa_48': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'pneumocystis_jiroveci': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'pseudomonas_aeruginosa': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'rhodococcus_equi': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'rsva': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'rsvb': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'senotophomonas_maltophilia': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'shv_esbl': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'staphylococcus_aureus': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'staphylococcus_mrsa': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'streptococcus_pneumoniae': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tem_esbl': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vim': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.secondarydiagnosis': {
            'Meta': {'object_name': 'SecondaryDiagnosis'},
            'co_primary': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.travel': {
            'Meta': {'object_name': 'Travel'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'dates': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'destination_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Destination']", 'null': 'True', 'blank': 'True'}),
            'destination_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'malaria_compliance': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'malaria_drug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial']", 'null': 'True', 'blank': 'True'}),
            'malaria_drug_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'malaria_prophylaxis': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
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
        u'opal.episode': {
            'Meta': {'object_name': 'Episode'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'inpatient'", 'max_length': '200'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_admission': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_episode': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
        u'opal.travel_reason': {
            'Meta': {'ordering': "['name']", 'object_name': 'Travel_reason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['elcid']