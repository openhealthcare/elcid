"""
ELCID implementation specific models!
"""
from django.db import models

from opal.models import (Subrecord, TaggedSubrecordMixin, option_models,
                         EpisodeSubrecord, PatientSubrecord)
from opal.utils.fields import ForeignKeyOrFreeText

__all__ = [
    'Location',
    'Demographics',
    'Diagnosis',
    'PastMedicalHistory',
    'GeneralNote',
    'Travel',
    'Antimicrobial',
    'MicrobiologyInput',
    'Todo',
    'MicrobiologyTest'
    ]

class Demographics(PatientSubrecord):
    _is_singleton = True

    name = models.CharField(max_length=255, blank=True)
    hospital_number = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)


class Location(TaggedSubrecordMixin, EpisodeSubrecord):
    _is_singleton = True

    category = models.CharField(max_length=255, blank=True)
    hospital = models.CharField(max_length=255, blank=True)
    ward = models.CharField(max_length=255, blank=True)
    bed = models.CharField(max_length=255, blank=True)


class Diagnosis(EpisodeSubrecord):
    _title = 'Diagnosis / Issues'
    _sort = 'date_of_diagnosis'

    condition = ForeignKeyOrFreeText(option_models['condition'])
    provisional = models.BooleanField()
    details = models.CharField(max_length=255, blank=True)
    date_of_diagnosis = models.DateField(blank=True, null=True)


class PastMedicalHistory(EpisodeSubrecord):
    _title = 'PMH'
    _sort = 'year'

    condition = ForeignKeyOrFreeText(option_models['condition'])
    year = models.CharField(max_length=4, blank=True)


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

    drug = ForeignKeyOrFreeText(option_models['antimicrobial'])
    dose = models.CharField(max_length=255, blank=True)
    route = ForeignKeyOrFreeText(option_models['antimicrobial_route'])
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class MicrobiologyInput(EpisodeSubrecord):
    _title = 'Clinical Advice'
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
    _title = 'Pathology Test'
    _sort = 'date_ordered'

    test = models.CharField(max_length=255)
    date_ordered = models.DateField(null=True, blank=True)
    details = models.CharField(max_length=255, blank=True)
    microscopy = models.CharField(max_length=255, blank=True)
    organism = models.CharField(max_length=255, blank=True)
    sensitive_antibiotics = models.CharField(max_length=255, blank=True)
    resistant_antibiotics = models.CharField(max_length=255, blank=True)
    result = models.CharField(max_length=20, blank=True)
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
