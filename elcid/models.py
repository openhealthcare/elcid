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
    'Demographics',
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
    'OPATReview',
    'OPATOutstandingIssues'
    ]


class Demographics(PatientSubrecord):
    _is_singleton = True
    _fieldnames = [
        'hospital_number', 'nhs_number',
        'name', 'date_of_birth',
        'country_of_birth', 'ethnicity'
        ]

    name = models.CharField(max_length=255, blank=True)
    hospital_number = models.CharField(max_length=255, blank=True)
    nhs_number = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country_of_birth = ForeignKeyOrFreeText(option_models['destination'])
    ethnicity = models.CharField(max_length=255, blank=True, null=True)


class ContactDetails(PatientSubrecord):
    _is_singleton = True

    address_line1 = models.CharField("Address line 1", max_length = 45,
                                     blank=True, null=True)
    address_line2 = models.CharField("Address line 2", max_length = 45,
                                     blank=True, null=True)
    city = models.CharField(max_length = 50, blank = True)
    county = models.CharField("County", max_length = 40,
                              blank=True, null=True)
    post_code = models.CharField("Post Code", max_length = 10,
                                 blank=True, null=True)
    tel1 = models.CharField(blank=True, null=True, max_length=50)
    tel2 = models.CharField(blank=True, null=True, max_length=50)


class Carers(PatientSubrecord):
    _is_singleton = True

    gp = models.ForeignKey(GP, blank=True, null=True)
    nurse = models.ForeignKey(CommunityNurse, blank=True, null=True)


#class Location(TaggedSubrecordMixin, EpisodeSubrecord):
class Location(EpisodeSubrecord):
    _is_singleton = True

    category = models.CharField(max_length=255, blank=True)
    hospital = models.CharField(max_length=255, blank=True)
    ward = models.CharField(max_length=255, blank=True)
    bed = models.CharField(max_length=255, blank=True)
    opat_referral_route = models.CharField(max_length=255, blank=True, null=True)
    opat_referral_team = models.CharField(max_length=255, blank=True, null=True)
    opat_referral = models.DateField(blank=True, null=True)
    opat_discharge = models.DateField(blank=True, null=True)

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
    _fieldnames = [
        'condition', 'provisional',
        'details', 'date_of_diagnosis'
        ]

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
    _fieldnames = [
        'condition', 'year', 'details'
        ]

    condition = ForeignKeyOrFreeText(option_models['condition'])
    year = models.CharField(max_length=4, blank=True)
    details = models.CharField(max_length=255, blank=True)


class GeneralNote(EpisodeSubrecord):
    _title = 'General Notes'
    _sort = 'date'

    date = models.DateField(null=True, blank=True)
    comment = models.TextField()


class Travel(EpisodeSubrecord):
    _fieldnames = [
        'destination', 'dates', 'reason_for_travel',
        'specific_exposures'
        ]

    destination = ForeignKeyOrFreeText(option_models['destination'])
    dates = models.CharField(max_length=255, blank=True)
    reason_for_travel = ForeignKeyOrFreeText(option_models['travel_reason'])
    specific_exposures = models.CharField(max_length=255, blank=True)


class Antimicrobial(EpisodeSubrecord):
    _title = 'Antimicrobials'
    _sort = 'start_date'
    _fieldnames = [
        'drug', 'start_date', 'end_date', 'dose',
        'route', 'delivered_by', 'adverse_event'
        ]

    drug = ForeignKeyOrFreeText(option_models['antimicrobial'])
    dose = models.CharField(max_length=255, blank=True)
    route = ForeignKeyOrFreeText(option_models['antimicrobial_route'])
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    delivered_by = models.CharField(max_length=255, blank=True, null=True)
    adverse_event = ForeignKeyOrFreeText(option_models['antimicrobial_adverse_event'])


class Allergies(PatientSubrecord):
    _fieldnames = [
        'drug', 'provisional', 'details'
        ]

    drug = ForeignKeyOrFreeText(option_models['antimicrobial'])
    provisional = models.BooleanField()
    details = models.CharField(max_length=255, blank=True)


class MicrobiologyInput(EpisodeSubrecord):
    _title = 'Clinical Advice'
    _sort = 'date'
    _fieldnames = [
        'date', 'initials', 'reason_for_interaction',
        'clinical_discussion', 'agreed_plan',
        'discussed_with',
        'clinical_advice_given', 'infection_control_advice_given',
        'change_in_antibiotic_prescription', 'referred_to_opat'
        ]

    date = models.DateField(null=True, blank=True)
    initials = models.CharField(max_length=255, blank=True)
    reason_for_interaction = ForeignKeyOrFreeText(option_models['clinical_advice_reason_for_interaction'])
    clinical_discussion = models.TextField(blank=True)
    agreed_plan = models.TextField(blank=True)
    discussed_with = models.CharField(max_length=255, blank=True)
    clinical_advice_given = models.BooleanField()
    infection_control_advice_given = models.BooleanField()
    change_in_antibiotic_prescription = models.BooleanField()
    referred_to_opat = models.BooleanField()


class Todo(EpisodeSubrecord):
    _title = 'To Do'
    details = models.TextField(blank=True)


class MicrobiologyTest(EpisodeSubrecord):
    _title = 'Investigations'
    _sort = 'date_ordered'
    _fieldnames = [
        'test',
        'date_ordered',
        'details',
        'microscopy',
        'organism',
        'sensitive_antibiotics',
        'resistant_antibiotics',
        'result',
        'igm',
        'igg',
        'vca_igm',
        'vca_igg',
        'ebna_igg',
        'hbsag',
        'anti_hbs',
        'anti_hbcore_igm',
        'anti_hbcore_igg',
        'rpr',
        'tppa',
        'viral_load',
        'parasitaemia',
        'hsv',
        'vzv',
        'syphilis',
        'c_difficile_antigen',
        'c_difficile_toxin',
        'species',
        'hsv_1',
        'hsv_2',
        'enterovirus',
        'cmv',
        'ebv',
        'influenza_a',
        'influenza_b',
        'parainfluenza',
        'metapneumovirus',
        'rsv',
        'adenovirus',
        'norovirus',
        'rotavirus',
        'giardia',
        'entamoeba_histolytica',
        'cryptosporidium',

        ]

    test = models.CharField(max_length=255)
    date_ordered = models.DateField(null=True, blank=True)
    details = models.CharField(max_length=255, blank=True)
    microscopy = models.CharField(max_length=255, blank=True)
    organism = models.CharField(max_length=255, blank=True)
    sensitive_antibiotics = models.CharField(max_length=255, blank=True)
    resistant_antibiotics = models.CharField(max_length=255, blank=True)
    result = models.CharField(max_length=255, blank=True)
    igm = models.CharField(max_length=20, blank=True)
    igg = models.CharField(max_length=20, blank=True)
    vca_igm = models.CharField(max_length=20, blank=True)
    vca_igg = models.CharField(max_length=20, blank=True)
    ebna_igg = models.CharField(max_length=20, blank=True)
    hbsag = models.CharField(max_length=20, blank=True)
    anti_hbs = models.CharField(max_length=20, blank=True)
    anti_hbcore_igm = models.CharField(max_length=20, blank=True)
    anti_hbcore_igg = models.CharField(max_length=20, blank=True)
    rpr = models.CharField(max_length=20, blank=True)
    tppa = models.CharField(max_length=20, blank=True)
    viral_load = models.CharField(max_length=20, blank=True)
    parasitaemia = models.CharField(max_length=20, blank=True)
    hsv = models.CharField(max_length=20, blank=True)
    vzv = models.CharField(max_length=20, blank=True)
    syphilis = models.CharField(max_length=20, blank=True)
    c_difficile_antigen = models.CharField(max_length=20, blank=True)
    c_difficile_toxin = models.CharField(max_length=20, blank=True)
    species = models.CharField(max_length=20, blank=True)
    hsv_1 = models.CharField(max_length=20, blank=True)
    hsv_2 = models.CharField(max_length=20, blank=True)
    enterovirus = models.CharField(max_length=20, blank=True)
    cmv = models.CharField(max_length=20, blank=True)
    ebv = models.CharField(max_length=20, blank=True)
    influenza_a = models.CharField(max_length=20, blank=True)
    influenza_b = models.CharField(max_length=20, blank=True)
    parainfluenza = models.CharField(max_length=20, blank=True)
    metapneumovirus = models.CharField(max_length=20, blank=True)
    rsv = models.CharField(max_length=20, blank=True)
    adenovirus = models.CharField(max_length=20, blank=True)
    norovirus = models.CharField(max_length=20, blank=True)
    rotavirus = models.CharField(max_length=20, blank=True)
    giardia = models.CharField(max_length=20, blank=True)
    entamoeba_histolytica = models.CharField(max_length=20, blank=True)
    cryptosporidium = models.CharField(max_length=20, blank=True)

"""
Begin OPAT specific fields.
"""

class Line(EpisodeSubrecord):
    _sort = 'insertion_date'

    line_type = ForeignKeyOrFreeText(option_models['line_type'])
    site = ForeignKeyOrFreeText(option_models['line_site'])
    insertion_date = models.DateField(blank=True, null=True)
    insertion_time = models.IntegerField(blank=True, null=True)
    inserted_by = models.CharField(max_length=255, blank=True, null=True)
    external_length = models.CharField(max_length=255, blank=True, null=True)
    removal_date = models.DateField(blank=True, null=True)
    removal_time = models.IntegerField(blank=True, null=True)
    complications = ForeignKeyOrFreeText(option_models['line_complication'])
    removal_reason = ForeignKeyOrFreeText(option_models['line_removal_reason'])
    special_instructions = models.TextField()


class OPATReview(EpisodeSubrecord):
    _sort = 'date'

    date = models.DateField(null=True, blank=True)
    initials = models.CharField(max_length=255, blank=True)
    rv_type = models.CharField(max_length=255, blank=True, null=True)
    discussion = models.TextField(blank=True, null=True)
    opat_plan = models.TextField(blank=True)
    next_review = models.DateField(blank=True, null=True)


class OPATOutstandingIssues(EpisodeSubrecord):
    _title = 'Outstanding Issues'
    details = models.TextField(blank=True)
