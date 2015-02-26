"""
ELCID implementation specific models!
"""
from django.db import models

from opal.models import (Subrecord,
                         option_models,
                         EpisodeSubrecord, PatientSubrecord, GP, CommunityNurse)
from opal.utils.fields import ForeignKeyOrFreeText
from opal.utils.models import lookup_list

class Demographics(PatientSubrecord):
    _is_singleton = True
    _icon = 'fa fa-user'
    
    name             = models.CharField(max_length=255, blank=True)
    hospital_number  = models.CharField(max_length=255, blank=True)
    nhs_number       = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth    = models.DateField(null=True, blank=True)
    country_of_birth = ForeignKeyOrFreeText(option_models['destination'])
    ethnicity        = models.CharField(max_length=255, blank=True, null=True)
    gender           = models.CharField(max_length=255, blank=True, null=True)


class ContactDetails(PatientSubrecord):
    _is_singleton = True
    _icon = 'fa fa-phone'

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

    gp    = models.ForeignKey(GP, blank=True, null=True)
    nurse = models.ForeignKey(CommunityNurse, blank=True, null=True)


class Location(EpisodeSubrecord):
    _is_singleton = True    
    _icon = 'fa fa-map-marker'
    
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
        try:
            demographics = self.episode.patient.demographics_set.get()
            return u'Location for {0}({1}) {2} {3} {4} {5}'.format(
                demographics.name,
                demographics.hospital_number,
                self.category,
                self.hospital,
                self.ward,
                self.bed
            )
        except:
            return 'demographics'


class PresentingComplaint(EpisodeSubrecord):
    _title = 'Presenting Complaint'
    _icon = 'fa fa-stethoscope'

    symptom  = ForeignKeyOrFreeText(option_models['symptom'])
    duration = models.CharField(max_length=255, blank=True, null=True)
    details  = models.CharField(max_length=255, blank=True, null=True)


class PrimaryDiagnosis(EpisodeSubrecord):
    """
    This is the confirmed primary diagnosisa
    """
    _is_singleton= True

    condition = ForeignKeyOrFreeText(option_models['condition'])
    confirmed = models.BooleanField(default=False)


class SecondaryDiagnosis(EpisodeSubrecord):
    """
    This is a confirmed diagnosis at discharge time.
    """
    condition   = ForeignKeyOrFreeText(option_models['condition'])
    co_primary = models.BooleanField(default=False)

    
class Diagnosis(EpisodeSubrecord):
    """
    This is a working-diagnosis list, will often contain things that are
    not technically diagnoses, but is for historical reasons, called diagnosis.
    """
    _title = 'Diagnosis / Issues'
    _sort = 'date_of_diagnosis'
    _icon = 'fa fa-stethoscope'

    condition         = ForeignKeyOrFreeText(option_models['condition'])
    provisional       = models.BooleanField()
    details           = models.CharField(max_length=255, blank=True)
    date_of_diagnosis = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'Diagnosis of {0} - {1}'.format(
            self.condition,
            self.date_of_diagnosis
            )


class PastMedicalHistory(EpisodeSubrecord):
    _title = 'PMH'
    _sort = 'year'
    _icon = 'fa fa-history'
    
    condition = ForeignKeyOrFreeText(option_models['condition'])
    year      = models.CharField(max_length=4, blank=True)
    details   = models.CharField(max_length=255, blank=True)


class GeneralNote(EpisodeSubrecord):
    _title = 'General Notes'
    _sort  = 'date'
    _icon = 'fa fa-info-circle'

    date    = models.DateField(null=True, blank=True)
    comment = models.TextField()


class Travel(EpisodeSubrecord):
    _icon = 'fa fa-plane'

    destination         = ForeignKeyOrFreeText(option_models['destination'])
    dates               = models.CharField(max_length=255, blank=True)
    reason_for_travel   = ForeignKeyOrFreeText(option_models['travel_reason'])
    specific_exposures  = models.CharField(max_length=255, blank=True)
    malaria_prophylaxis = models.BooleanField(default=False)
    malaria_drug        = ForeignKeyOrFreeText(option_models['antimicrobial'])
    malaria_compliance  = models.CharField(max_length=200, blank=True, null=True)

ReasonForStoppingLookupList = type(*lookup_list('iv_stop', module=__name__))
DrugDeliveredLookupList = type(*lookup_list('drug_delivered', module=__name__))

class Antimicrobial(EpisodeSubrecord):
    _title = 'Antimicrobials'
    _sort = 'start_date'
    _icon = 'fa fa-flask'
    _modal = 'lg'
    
    drug          = ForeignKeyOrFreeText(option_models['antimicrobial'])
    dose          = models.CharField(max_length=255, blank=True)
    route         = ForeignKeyOrFreeText(option_models['antimicrobial_route'])
    start_date    = models.DateField(null=True, blank=True)
    end_date      = models.DateField(null=True, blank=True)
    delivered_by  = ForeignKeyOrFreeText(DrugDeliveredLookupList)
    reason_for_stopping = ForeignKeyOrFreeText(ReasonForStoppingLookupList)
    adverse_event = ForeignKeyOrFreeText(option_models['antimicrobial_adverse_event'])
    comments      = models.TextField(blank=True, null=True)
    frequency     = ForeignKeyOrFreeText(option_models['antimicrobial_frequency'])

class Allergies(PatientSubrecord):
    _icon = 'fa fa-warning'
    
    drug        = ForeignKeyOrFreeText(option_models['antimicrobial'])
    provisional = models.BooleanField()
    details     = models.CharField(max_length=255, blank=True)


class MicrobiologyInput(EpisodeSubrecord):
    _title = 'Clinical Advice'
    _sort = 'date'
    _icon = 'fa fa-comments'
    _modal = 'lg'
    _list_limit = 3

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
    _icon = 'fa fa-th-list'
    
    details = models.TextField(blank=True)


class MicrobiologyTest(EpisodeSubrecord):
    _title = 'Investigations'
    _sort = 'date_ordered'
    _icon = 'fa fa-crosshairs'
    _modal = 'lg'
    
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

OPATUnplannedStopLookupList = type(*lookup_list('unplanned_stop', module=__name__))
OPATReviewTypeLookupList = type(*lookup_list('opat_rvt', module=__name__))

class OPATMeta(EpisodeSubrecord):
    review_date           = models.DateField(blank=True, null=True)
    reason_for_stopping   = models.CharField(max_length=200, blank=True, null=True)
    unplanned_stop_reason = ForeignKeyOrFreeText(OPATUnplannedStopLookupList)
    stopping_iv_details   = models.CharField(max_length=200, blank=True, null=True)
    treatment_outcome     = models.CharField(max_length=200, blank=True, null=True)
    deceased              = models.BooleanField(default=False)
    death_category        = models.CharField(max_length=200, blank=True, null=True)
    cause_of_death        = models.CharField(max_length=200, blank=True, null=True)
    readmitted            = models.BooleanField(default=False)
    readmission_cause     = models.CharField(max_length=200, blank=True, null=True)
    notes                 = models.TextField(blank=True, null=True)


class OPATOutcome(EpisodeSubrecord):
    """
    This captures the final data for an OAPT episode - it is much the
    same as OPAT meta data, but captured on the ward round and interrogated
    differently. 
    """
    _is_singleton     = True

    treatment_outcome     = models.CharField(max_length=200, blank=True, null=True)
    deceased              = models.BooleanField(default=False)
    death_category        = models.CharField(max_length=200, blank=True, null=True)
    cause_of_death        = models.CharField(max_length=200, blank=True, null=True)
    readmitted            = models.BooleanField(default=False)
    readmission_cause     = models.CharField(max_length=200, blank=True, null=True)
    notes                 = models.TextField(blank=True, null=True)
    patient_feedback      = models.BooleanField(default=False)
    

class OPATRejection(EpisodeSubrecord):

    decided_by            = models.CharField(max_length=255, blank=True, null=True)
    patient_choice        = models.BooleanField(default=False)
    oral_available        = models.BooleanField(default=False)
    not_needed            = models.BooleanField(default=False)
    patient_suitability   = models.BooleanField(default=False)
    not_fit_for_discharge = models.BooleanField(default=False)
    non_complex_infection = models.BooleanField(default=False)
    no_social_support     = models.BooleanField(default=False)
    reason                = models.CharField(max_length=255, blank=True, null=True)
    date                  = models.DateField(blank=True, null=True)


class Line(EpisodeSubrecord):
    _sort = 'insertion_datetime'
    _icon = 'fa fa-bolt'

    line_type            = ForeignKeyOrFreeText(option_models['line_type'])
    site                 = ForeignKeyOrFreeText(option_models['line_site'])
    insertion_datetime   = models.DateTimeField(blank=True, null=True)
    inserted_by          = models.CharField(max_length=255, blank=True, null=True)
    external_length      = models.CharField(max_length=255, blank=True, null=True)
    removal_datetime     = models.DateTimeField(blank=True, null=True)
    complications        = ForeignKeyOrFreeText(option_models['line_complication'])
    removal_reason       = ForeignKeyOrFreeText(option_models['line_removal_reason'])
    special_instructions = models.TextField()


class OPATReview(EpisodeSubrecord):
    _sort = 'datetime'
    _title = 'OPAT Review'
    _icon = 'fa fa-comments'
    _list_limit = 1

    datetime                = models.DateTimeField(null=True, blank=True)
    initials                = models.CharField(max_length=255, blank=True)
    rv_type                 = ForeignKeyOrFreeText(OPATReviewTypeLookupList)
    discussion              = models.TextField(blank=True, null=True)
    opat_plan               = models.TextField(blank=True)
    next_review             = models.DateField(blank=True, null=True)    
    dressing_changed        = models.BooleanField(default=False)
    bung_changed            = models.BooleanField(default=False)
    medication_administered = models.TextField(blank=True, null=True)
    adverse_events          = ForeignKeyOrFreeText(option_models['antimicrobial_adverse_event'])


class OPATOutstandingIssues(EpisodeSubrecord):
    _title = 'Outstanding Issues'
    _icon = 'fa fa-th-list'

    details = models.TextField(blank=True)


class Appointment(EpisodeSubrecord):
    _title = 'Upcoming Appointments'
    _sort = 'date'
    _icon = 'fa fa-calendar'

    appointment_type = models.CharField(max_length=200, blank=True, null=True)
    appointment_with = models.CharField(max_length=200, blank=True, null=True)
    date             = models.DateField(blank=True, null=True)


class OPATLineAssessment(EpisodeSubrecord):    
    _title = 'OPAT Line Assessment'
    _icon = 'fa fa-check-square-o'

    line                   = models.CharField(max_length=200, blank=True, null=True)
    assessment_date        = models.DateField(blank=True, null=True)
    vip_score              = models.IntegerField(blank=True, null=True)
    dressing_type          = models.CharField(max_length=200, blank=True, null=True)
    dressing_change_date   = models.DateField(blank=True, null=True)
    dressing_change_reason = models.CharField(max_length=200, blank=True, null=True)
    bionector_change_date  = models.DateField(blank=True, null=True)
    dressing_intact        = models.BooleanField(default=False)
    lumen_flush_ok         = models.BooleanField(default=False)
    blood_drawback_seen    = models.BooleanField(default=False)
    cm_from_exit_site      = models.BooleanField(default=False)


"""
Fields for UCLH - specific Research studies.
"""

""" RiD RTI (http://www.rid-rti.eu/ ) """
SpeciminLookupList = type(*lookup_list('specimin', module=__name__))
SpeciminAppearanceLookupList = type(*lookup_list('specimin_appearance', module=__name__))
OrganismDetailsLookupList = type(*lookup_list('organism_details', module=__name__))
AntimicrobialSusceptabilityLookupList = type(*lookup_list('antimicrobial_susceptability', module=__name__))
CheckpointsAssayLookupList = type(*lookup_list('checkpoints_assay', module=__name__))


class LabSpecimin(EpisodeSubrecord):
    _title = 'Lab Specimen'
    _sort = 'date_collected'

    specimin_type     = ForeignKeyOrFreeText(SpeciminLookupList)
    date_collected    = models.DateField(blank=True, null=True)
    volume            = models.CharField(max_length=200, blank=True, null=True)
    appearance        = ForeignKeyOrFreeText(SpeciminAppearanceLookupList)
    epithelial_cell   = models.CharField(max_length=200, blank=True, null=True)
    white_blood_cells = models.CharField(max_length=200, blank=True, null=True)
    date_tested       = models.DateField(blank=True, null=True)
    external_id       = models.CharField(max_length=200, blank=True, null=True)
    biobanking        = models.BooleanField(default=False)
    biobanking_box    = models.CharField(max_length=200, blank=True, null=True)
    date_biobanked    = models.DateField(blank=True, null=True)
    volume_biobanked  = models.CharField(max_length=200, blank=True, null=True)


# This is based on the investigations record type from elCID
class LabTest(EpisodeSubrecord):
    _sort = 'date_ordered'

    """
    Begin elCID.models.investigations fields
    """

    test                         = models.CharField(max_length=255)
    date_ordered                 = models.DateField(null=True, blank=True)
    details                      = models.CharField(max_length=255, blank=True)
    result                       = models.CharField(max_length=255, blank=True)
    significant_organism         = models.BooleanField(default=False)
    organism_details             = ForeignKeyOrFreeText(OrganismDetailsLookupList)
    antimicrobial_susceptability = ForeignKeyOrFreeText(AntimicrobialSusceptabilityLookupList)
    retrieved                    = models.BooleanField(default=False)
    date_retrieved               = models.DateField(null=True, blank=True)
    biobanked                    = models.BooleanField(default=False)
    freezer_box_number           = models.CharField(max_length=200, blank=True, null=True)
    esbl                         = models.BooleanField(default=False)
    carbapenemase                = models.BooleanField(default=False)


class RidRTITest(EpisodeSubrecord):
    """
    Results of the actual RiD RTI test ! 
    """
    test            = models.CharField(max_length=200, blank=True, null=True)
    notes           = models.TextField(blank=True, null=True)
    # HAP/VAP results
    pseudomonas_aeruginosa = models.BooleanField(default=False)
    acinetobacter_baumannii = models.BooleanField(default=False)
    senotophomonas_maltophilia = models.BooleanField(default=False)
    klebsiella_spp = models.BooleanField(default=False)
    enterobacter_spp = models.BooleanField(default=False)
    staphylococcus_aureus = models.BooleanField(default=False)
    staphylococcus_mrsa = models.BooleanField(default=False)
    ctx_m = models.BooleanField(default=False)
    shv_esbl = models.BooleanField(default=False)
    tem_esbl = models.BooleanField(default=False)
    vim = models.BooleanField(default=False)
    imp = models.BooleanField(default=False)
    ndm = models.BooleanField(default=False)
    kpc = models.BooleanField(default=False)
    oxa_48 = models.BooleanField(default=False)
    meca = models.BooleanField(default=False)
    # CAP results
    mycoplasma_pneumoniae = models.BooleanField(default=False)
    chlamydophila_pneumoniae = models.BooleanField(default=False)
    legionella_pneumophila = models.BooleanField(default=False)
    # (Mycobacterium tuberculosis complex) = models.BooleanField(default=False)
    mtc = models.BooleanField(default=False)
    haemophilus_influenzae = models.BooleanField(default=False)
    streptococcus_pneumoniae = models.BooleanField(default=False)
    rsva = models.BooleanField(default=False)
    rsvb = models.BooleanField(default=False)
    influenza_a = models.BooleanField(default=False)
    influenza_b      = models.BooleanField(default=False)
    cap_coronavirus_oc43 = models.BooleanField(default=False)
    cap_coronavirus_hku1 = models.BooleanField(default=False)
    cap_coronavirus_nl63 = models.BooleanField(default=False)
    cap_coronavirus_229e = models.BooleanField(default=False)
    # ORTI results
    nocardia_spp = models.BooleanField(default=False)
    rhodococcus_equi = models.BooleanField(default=False)
    # (Aspergillus spp Cryptococcus neoformans)
    aspergillus_spp = models.BooleanField(default=False)
    cryptococcus_neoformans = models.BooleanField(default=False)
    pneumocystis_jiroveci = models.BooleanField(default=False)
    orti_coronavirus_oc43 = models.BooleanField(default=False)
    orti_coronavirus_hku1 = models.BooleanField(default=False)
    orti_coronavirus_nl63 = models.BooleanField(default=False)
    orti_coronavirus_229e = models.BooleanField(default=False)

class CheckpointsAssay(EpisodeSubrecord):
    _is_singleton = True

    acc = models.BooleanField(default=False)
    act_mir = models.BooleanField(default=False)
    bel = models.BooleanField(default=False)
    cmy_i_mox = models.BooleanField(default=False)
    cmy_ii = models.BooleanField(default=False)
    ctx_m_1_group = models.BooleanField(default=False)
    ctx_m_1_like = models.BooleanField(default=False)
    ctx_m_15_like = models.BooleanField(default=False)
    ctx_m_2_group = models.BooleanField(default=False)
    ctx_m_3_like = models.BooleanField(default=False)
    ctx_m_32_like = models.BooleanField(default=False)
    ctx_m_8_25_group = models.BooleanField(default=False)
    ctx_m_9_group = models.BooleanField(default=False)
    dha = models.BooleanField(default=False)
    fox = models.BooleanField(default=False)
    ges = models.BooleanField(default=False)
    gim = models.BooleanField(default=False)
    imp = models.BooleanField(default=False)
    kpc = models.BooleanField(default=False)
    ndm = models.BooleanField(default=False)
    oxa_23_like = models.BooleanField(default=False)
    oxa_24_like = models.BooleanField(default=False)
    oxa_48_like = models.BooleanField(default=False)
    oxa_58_like = models.BooleanField(default=False)
    per = models.BooleanField(default=False)
    shv_e240k = models.BooleanField(default=False)
    shv_g238a = models.BooleanField(default=False)
    shv_g238s = models.BooleanField(default=False)
    shv_wt = models.BooleanField(default=False)
    spm = models.BooleanField(default=False)
    tem_e104k = models.BooleanField(default=False)
    tem_g238s = models.BooleanField(default=False)
    tem_r164c = models.BooleanField(default=False)
    tem_r164h = models.BooleanField(default=False)
    tem_r164s = models.BooleanField(default=False)
    tem_wt = models.BooleanField(default=False)
    veb = models.BooleanField(default=False)
    vim = models.BooleanField(default=False)
    
    negative = models.BooleanField(default=False)
    comments = models.TextField(blank=True, null=True)
