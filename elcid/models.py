"""
ELCID implementation specific models!
"""
from django.db import models

from opal.models import (Subrecord,
#                         TaggedSubrecordMixin,
                         option_models,
                         EpisodeSubrecord, PatientSubrecord, GP, CommunityNurse)
from opal.utils.fields import ForeignKeyOrFreeText

__all__ = [
    'Demographcs',
    'ContactDetails',
    'Carers',
    'Location',
    'Allergies',
    'Diagnosis',
    'PastMedicalHistory',
    'GeneralNote',
    'Travel',
    'Antimicrobial',
    'MicrobiologyInput',
    'Todo',
    'MicrobiologyTest',
    'Line',
    'Appointment',
    'OPATReview',
    'OPATOutstandingIssues',
    'OPATLineAssessment',
    ]


class Demographics(PatientSubrecord):
    _is_singleton = True

    name             = models.CharField(max_length=255, blank=True)
    hospital_number  = models.CharField(max_length=255, blank=True)
    nhs_number       = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth    = models.DateField(null=True, blank=True)
    country_of_birth = ForeignKeyOrFreeText(option_models['destination'])
    ethnicity        = models.CharField(max_length=255, blank=True, null=True)
    gender           = models.CharField(max_length=255, blank=True, null=True)


class ContactDetails(PatientSubrecord):
    _is_singleton = True
    _episode_category = 'OPAT'

    address_line1 = models.CharField("Address line 1", max_length = 45,
                                     blank=True, null=True)
    address_line2 = models.CharField("Address line 2", max_length = 45,
                                     blank=True, null=True)
    city          = models.CharField(max_length = 50, blank = True)
    county        = models.CharField("County", max_length = 40,
                                     blank=True, null=True)
    post_code     = models.CharField("Post Code", max_length = 10,
                                     blank=True, null=True)
    tel1          = models.CharField(blank=True, null=True, max_length=50)
    tel2          = models.CharField(blank=True, null=True, max_length=50)


class Carers(PatientSubrecord):
    _is_singleton = True
    _episode_category = 'OPAT'

    gp    = models.ForeignKey(GP, blank=True, null=True)
    nurse = models.ForeignKey(CommunityNurse, blank=True, null=True)


#class Location(TaggedSubrecordMixin, EpisodeSubrecord):
class Location(EpisodeSubrecord):
    _is_singleton = True

    category                   = models.CharField(max_length=255, blank=True)
    hospital                   = models.CharField(max_length=255, blank=True)
    ward                       = models.CharField(max_length=255, blank=True)
    bed                        = models.CharField(max_length=255, blank=True)
    opat_referral_route        = models.CharField(max_length=255, blank=True, null=True)
    opat_referral_team         = models.CharField(max_length=255, blank=True, null=True)
    opat_referral_consultant   = models.CharField(max_length=255, blank=True, null=True)
    opat_referral_team_address = models.TextField(blank=True, null=True)
    opat_referral              = models.DateField(blank=True, null=True)
    opat_discharge             = models.DateField(blank=True, null=True)

    def __unicode__(self):
        demographics = self.episode.patient.demographics_set.get()
        return u'Location for {0}({1}) {2} {3} {4} {5}'.format(
            demographics.name,
            demographics.hospital_number,
            self.category,
            self.hospital,
            self.ward,
            self.bed
            )


class Diagnosis(EpisodeSubrecord):
    _title = 'Diagnosis / Issues'
    _sort = 'date_of_diagnosis'

    condition = ForeignKeyOrFreeText(option_models['condition'])
    provisional = models.BooleanField()
    details = models.CharField(max_length=255, blank=True)
    date_of_diagnosis = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'Diagnosis for {0}: {1} - {2}'.format(
            self.episode.patient.demographics_set.get().name,
            self.condition,
            self.date_of_diagnosis
            )


class PastMedicalHistory(EpisodeSubrecord):
    _title = 'PMH'
    _sort = 'year'

    condition = ForeignKeyOrFreeText(option_models['condition'])
    year = models.CharField(max_length=4, blank=True)
    details = models.CharField(max_length=255, blank=True)


class GeneralNote(EpisodeSubrecord):
    _title = 'General Notes'
    _sort = 'date'

    date = models.DateField(null=True, blank=True)
    comment = models.TextField()


class Travel(EpisodeSubrecord):
    destination = ForeignKeyOrFreeText(option_models['destination'])
    dates = models.CharField(max_length=255, blank=True)
    reason_for_travel = ForeignKeyOrFreeText(option_models['travel_reason'])
    specific_exposures = models.CharField(max_length=255, blank=True)


class Antimicrobial(EpisodeSubrecord):
    _title = 'Antimicrobials'
    _sort = 'start_date'

    drug          = ForeignKeyOrFreeText(option_models['antimicrobial'])
    dose          = models.CharField(max_length=255, blank=True)
    route         = ForeignKeyOrFreeText(option_models['antimicrobial_route'])
    start_date    = models.DateField(null=True, blank=True)
    end_date      = models.DateField(null=True, blank=True)
    delivered_by  = models.CharField(max_length=255, blank=True, null=True)
    adverse_event = ForeignKeyOrFreeText(option_models['antimicrobial_adverse_event'])
    comments      = models.TextField(blank=True, null=True)
    frequency     = ForeignKeyOrFreeText(option_models['antimicrobial_frequency'])

class Allergies(PatientSubrecord):

    drug        = ForeignKeyOrFreeText(option_models['antimicrobial'])
    provisional = models.BooleanField()
    details     = models.CharField(max_length=255, blank=True)


class MicrobiologyInput(EpisodeSubrecord):
    _title = 'Clinical Advice'
    _sort = 'date'
    _read_only = 'true'

    date                              = models.DateField(null=True, blank=True)
    initials                          = models.CharField(max_length=255, blank=True)
    reason_for_interaction            = ForeignKeyOrFreeText(
        option_models['clinical_advice_reason_for_interaction'])
    clinical_discussion               = models.TextField(blank=True)
    agreed_plan                       = models.TextField(blank=True)
    discussed_with                    = models.CharField(max_length=255, blank=True)
    clinical_advice_given             = models.BooleanField()
    infection_control_advice_given    = models.BooleanField()
    change_in_antibiotic_prescription = models.BooleanField()
    referred_to_opat                  = models.BooleanField()


class Todo(EpisodeSubrecord):
    _title = 'To Do'
    details = models.TextField(blank=True)


class MicrobiologyTest(EpisodeSubrecord):
    _title = 'Investigations'
    _sort = 'date_ordered'

    test                  = models.CharField(max_length=255)
    date_ordered          = models.DateField(null=True, blank=True)
    details               = models.CharField(max_length=255, blank=True)
    microscopy            = models.CharField(max_length=255, blank=True)
    organism              = models.CharField(max_length=255, blank=True)
    sensitive_antibiotics = models.CharField(max_length=255, blank=True)
    resistant_antibiotics = models.CharField(max_length=255, blank=True)
    result                = models.CharField(max_length=255, blank=True)
    igm                   = models.CharField(max_length=20, blank=True)
    igg                   = models.CharField(max_length=20, blank=True)
    vca_igm               = models.CharField(max_length=20, blank=True)
    vca_igg               = models.CharField(max_length=20, blank=True)
    ebna_igg              = models.CharField(max_length=20, blank=True)
    hbsag                 = models.CharField(max_length=20, blank=True)
    anti_hbs              = models.CharField(max_length=20, blank=True)
    anti_hbcore_igm       = models.CharField(max_length=20, blank=True)
    anti_hbcore_igg       = models.CharField(max_length=20, blank=True)
    rpr                   = models.CharField(max_length=20, blank=True)
    tppa                  = models.CharField(max_length=20, blank=True)
    viral_load            = models.CharField(max_length=20, blank=True)
    parasitaemia          = models.CharField(max_length=20, blank=True)
    hsv                   = models.CharField(max_length=20, blank=True)
    vzv                   = models.CharField(max_length=20, blank=True)
    syphilis              = models.CharField(max_length=20, blank=True)
    c_difficile_antigen   = models.CharField(max_length=20, blank=True)
    c_difficile_toxin     = models.CharField(max_length=20, blank=True)
    species               = models.CharField(max_length=20, blank=True)
    hsv_1                 = models.CharField(max_length=20, blank=True)
    hsv_2                 = models.CharField(max_length=20, blank=True)
    enterovirus           = models.CharField(max_length=20, blank=True)
    cmv                   = models.CharField(max_length=20, blank=True)
    ebv                   = models.CharField(max_length=20, blank=True)
    influenza_a           = models.CharField(max_length=20, blank=True)
    influenza_b           = models.CharField(max_length=20, blank=True)
    parainfluenza         = models.CharField(max_length=20, blank=True)
    metapneumovirus       = models.CharField(max_length=20, blank=True)
    rsv                   = models.CharField(max_length=20, blank=True)
    adenovirus            = models.CharField(max_length=20, blank=True)
    norovirus             = models.CharField(max_length=20, blank=True)
    rotavirus             = models.CharField(max_length=20, blank=True)
    giardia               = models.CharField(max_length=20, blank=True)
    entamoeba_histolytica = models.CharField(max_length=20, blank=True)
    cryptosporidium       = models.CharField(max_length=20, blank=True)

"""
Begin OPAT specific fields.
"""

class OPATRejection(EpisodeSubrecord):
    _episode_category = 'OPAT'
    
    decided_by = models.CharField(max_length=255, blank=True, null=True)
    reason     = models.CharField(max_length=255, blank=True, null=True)
    date       = models.DateField(blank=True, null=True)


class Line(EpisodeSubrecord):
    _sort = 'insertion_date'
    _episode_category = 'OPAT'
    
    line_type            = ForeignKeyOrFreeText(option_models['line_type'])
    site                 = ForeignKeyOrFreeText(option_models['line_site'])
    insertion_date       = models.DateField(blank=True, null=True)
    insertion_time       = models.IntegerField(blank=True, null=True)
    inserted_by          = models.CharField(max_length=255, blank=True, null=True)
    external_length      = models.CharField(max_length=255, blank=True, null=True)
    removal_date         = models.DateField(blank=True, null=True)
    removal_time         = models.IntegerField(blank=True, null=True)
    complications        = ForeignKeyOrFreeText(option_models['line_complication'])
    removal_reason       = ForeignKeyOrFreeText(option_models['line_removal_reason'])
    special_instructions = models.TextField()


class OPATReview(EpisodeSubrecord):
    _sort = 'date'
    _episode_category = 'OPAT'
    _read_only = 'true'

    date        = models.DateField(null=True, blank=True)
    initials    = models.CharField(max_length=255, blank=True)
    rv_type     = models.CharField(max_length=255, blank=True, null=True)
    discussion  = models.TextField(blank=True, null=True)
    opat_plan   = models.TextField(blank=True)
    next_review = models.DateField(blank=True, null=True)


class OPATOutstandingIssues(EpisodeSubrecord):
    _title = 'Outstanding Issues'
    _episode_category = 'OPAT'
    details = models.TextField(blank=True)


class Appointment(EpisodeSubrecord):
    _title = 'Upcoming Appointments'
    _sort = 'date'
    _episode_category = 'OPAT'

    appointment_type = models.CharField(max_length=200, blank=True, null=True)
    appointment_with = models.CharField(max_length=200, blank=True, null=True)
    date             = models.DateField(blank=True, null=True)
    
    
class OPATLineAssessment(EpisodeSubrecord):
    _episode_category = 'OPAT'
    
    assessment_date = models.DateField(blank=True, null=True)
    vip_score = models.IntegerField(blank=True, null=True)
    dressing_type = models.CharField(max_length=200, blank=True, null=True)
    dressing_change_date = models.DateField(blank=True, null=True)
    dressing_change_reason = models.CharField(max_length=200, blank=True, null=True)
    bionector_change_date = models.DateField(blank=True, null=True)
