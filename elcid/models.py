"""
ELCID implementation specific models!
"""
from django.db import models

from opal.models import Subrecord, option_models
from opal.utils.fields import ForeignKeyOrFreeText

__all__ = [
    'Location',
    'Diagnosis',
    'PastMedicalHistory',
    'GeneralNote',
    'Travel',
    'Antimicrobial',
    'MicrobiologyInput',
    'Todo',
    'MicrobiologyTest'
    ]

class Demographics(Subrecord):
    _is_singleton = True

    name = models.CharField(max_length=255, blank=True)
    hospital_number = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)


class Location(Subrecord):
    _is_singleton = True

    @classmethod
    def _get_fieldnames_to_serialize(cls):
        fieldnames = super(Location, cls)._get_fieldnames_to_serialize()
        fieldnames.append('tags')
        return fieldnames

    @classmethod
    def get_field_type_for_tags(cls):
        return 'list'

    def get_tags(self):
        return {tag_name: True for tag_name in self.patient.get_tag_names()}

    # value is a dictionary mapping tag names to a boolean
    def set_tags(self, value, user):
        tags = [k for k, v in value.items() if v]
        self.patient.set_tags(tags, user)

    category = models.CharField(max_length=255, blank=True)
    hospital = models.CharField(max_length=255, blank=True)
    ward = models.CharField(max_length=255, blank=True)
    bed = models.CharField(max_length=255, blank=True)
    date_of_admission = models.DateField(null=True, blank=True)
    discharge_date = models.DateField(null=True, blank=True) # TODO rename to date_of_discharge?


class Diagnosis(Subrecord):
    _title = 'Diagnosis / Issues'
    condition = ForeignKeyOrFreeText(option_models['condition'])
    provisional = models.BooleanField()
    details = models.CharField(max_length=255, blank=True)
    date_of_diagnosis = models.DateField(blank=True, null=True)


class PastMedicalHistory(Subrecord):
    _title = 'PMH'
    condition = ForeignKeyOrFreeText(option_models['condition'])
    year = models.CharField(max_length=4, blank=True)


class GeneralNote(Subrecord):
    _title = 'General Notes'
    date = models.DateField(null=True, blank=True)
    comment = models.TextField()


class Travel(Subrecord):
    destination = ForeignKeyOrFreeText(option_models['destination'])
    dates = models.CharField(max_length=255, blank=True)
    reason_for_travel = ForeignKeyOrFreeText(option_models['travel_reason'])
    specific_exposures = models.CharField(max_length=255, blank=True)


class Antimicrobial(Subrecord):
    _title = 'Antimicrobials'
    drug = ForeignKeyOrFreeText(option_models['antimicrobial'])
    dose = models.CharField(max_length=255, blank=True)
    route = ForeignKeyOrFreeText(option_models['antimicrobial_route'])
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class MicrobiologyInput(Subrecord):
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


class Todo(Subrecord):
    _title = 'To Do'
    details = models.TextField(blank=True)


class MicrobiologyTest(Subrecord):
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
