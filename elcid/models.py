"""
elCID implementation specific models!
"""
from django.db import models

import opal.models as omodels

from opal.models import (
    EpisodeSubrecord, PatientSubrecord, GP, CommunityNurse, Episode, Team,
    Tagging
)
from opal.core.fields import ForeignKeyOrFreeText
from opal.core import lookuplists
from constants import MICROHAEM_CONSULTATIONS, MICROHAEM_TEAM_NAME


class Demographics(PatientSubrecord):
    _is_singleton = True
    _icon = 'fa fa-user'

    name             = models.CharField(max_length=255, blank=True)
    hospital_number  = models.CharField(max_length=255, blank=True)
    nhs_number       = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth    = models.DateField(null=True, blank=True)
    country_of_birth = ForeignKeyOrFreeText(omodels.Destination)
    ethnicity        = models.CharField(max_length=255, blank=True, null=True)
    gender           = models.CharField(max_length=255, blank=True, null=True)

    pid_fields       = 'name', 'hospital_number', 'nhs_number'

    class Meta:
        verbose_name_plural = "Demographics"


class ContactDetails(PatientSubrecord):
    _is_singleton = True
    _advanced_searchable = False
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

    class Meta:
        verbose_name_plural = "Contact details"


class Carers(PatientSubrecord):
    _is_singleton = True
    _advanced_searchable = False

    gp    = models.ForeignKey(GP, blank=True, null=True)
    nurse = models.ForeignKey(CommunityNurse, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Carers"


class Location(EpisodeSubrecord):
    _is_singleton = True
    _icon = 'fa fa-map-marker'

    category                   = models.CharField(max_length=255, blank=True)
    hospital                   = models.CharField(max_length=255, blank=True)
    ward                       = models.CharField(max_length=255, blank=True)
    bed                        = models.CharField(max_length=255, blank=True)
    opat_referral_route        = models.CharField(max_length=255, blank=True,
                                                  null=True)
    opat_referral_team         = models.CharField(max_length=255, blank=True,
                                                  null=True)
    opat_referral_consultant   = models.CharField(max_length=255, blank=True,
                                                  null=True)
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

    symptom  = ForeignKeyOrFreeText(omodels.Symptom)
    duration = models.CharField(max_length=255, blank=True, null=True)
    details  = models.CharField(max_length=255, blank=True, null=True)


class PrimaryDiagnosis(EpisodeSubrecord):
    """
    This is the confirmed primary diagnosisa
    """
    _is_singleton= True

    condition = ForeignKeyOrFreeText(omodels.Condition)
    confirmed = models.NullBooleanField(default=False)

    class Meta:
        verbose_name_plural = "Primary diagnoses"


class SecondaryDiagnosis(EpisodeSubrecord):
    """
    This is a confirmed diagnosis at discharge time.
    """
    condition   = ForeignKeyOrFreeText(omodels.Condition)
    co_primary = models.NullBooleanField(default=False)

    class Meta:
        verbose_name_plural = "Secondary diagnoses"


class Diagnosis(EpisodeSubrecord):
    """
    This is a working-diagnosis list, will often contain things that are
    not technically diagnoses, but is for historical reasons, called diagnosis.
    """
    _title = 'Diagnosis / Issues'
    _sort = 'date_of_diagnosis'
    _icon = 'fa fa-stethoscope'

    condition         = ForeignKeyOrFreeText(omodels.Condition)
    provisional       = models.NullBooleanField()
    details           = models.CharField(max_length=255, blank=True)
    date_of_diagnosis = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'Diagnosis of {0} - {1}'.format(
            self.condition,
            self.date_of_diagnosis
            )

    class Meta:
        verbose_name_plural = "Diagnoses"


class PastMedicalHistory(EpisodeSubrecord):
    _title = 'PMH'
    _sort = 'year'
    _icon = 'fa fa-history'

    condition = ForeignKeyOrFreeText(omodels.Condition)
    year      = models.CharField(max_length=200, blank=True)
    details   = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Past medical histories"


class GeneralNote(EpisodeSubrecord):
    _title = 'General Notes'
    _sort  = 'date'
    _icon = 'fa fa-info-circle'

    date    = models.DateField(null=True, blank=True)
    comment = models.TextField()


class Travel(EpisodeSubrecord):
    _icon = 'fa fa-plane'

    destination         = ForeignKeyOrFreeText(omodels.Destination)
    dates               = models.CharField(max_length=255, blank=True)
    reason_for_travel   = ForeignKeyOrFreeText(omodels.Travel_reason)
    did_not_travel      = models.NullBooleanField(default=False)
    specific_exposures  = models.CharField(max_length=255, blank=True)
    malaria_prophylaxis = models.NullBooleanField(default=False)
    malaria_drug        = ForeignKeyOrFreeText(omodels.Antimicrobial)
    malaria_compliance  = models.CharField(max_length=200, blank=True, null=True)


class Iv_stop(lookuplists.LookupList):
    class Meta:
        verbose_name = "IV stop"


class Drug_delivered(lookuplists.LookupList):
    class Meta:
        verbose_name_plural = "Drugs delivered"


class Antimicrobial(EpisodeSubrecord):
    _title = 'Antimicrobials'
    _sort = 'start_date'
    _icon = 'fa fa-flask'
    _modal = 'lg'

    drug          = ForeignKeyOrFreeText(omodels.Antimicrobial)
    dose          = models.CharField(max_length=255, blank=True)
    route         = ForeignKeyOrFreeText(omodels.Antimicrobial_route)
    start_date    = models.DateField(null=True, blank=True)
    end_date      = models.DateField(null=True, blank=True)
    delivered_by  = ForeignKeyOrFreeText(Drug_delivered)
    reason_for_stopping = ForeignKeyOrFreeText(Iv_stop)
    adverse_event = ForeignKeyOrFreeText(omodels.Antimicrobial_adverse_event)
    comments      = models.TextField(blank=True, null=True)
    frequency     = ForeignKeyOrFreeText(omodels.Antimicrobial_frequency)

class Allergies(PatientSubrecord):
    _icon = 'fa fa-warning'

    drug        = ForeignKeyOrFreeText(omodels.Antimicrobial)
    provisional = models.NullBooleanField()
    details     = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Allergies"


class MicrobiologyInput(EpisodeSubrecord):
    _title = 'Clinical Advice'
    _sort = 'when'
    _icon = 'fa fa-comments'
    _modal = 'lg'
    _list_limit = 3

    when = models.DateTimeField(null=True, blank=True)
    initials = models.CharField(max_length=255, blank=True)
    reason_for_interaction = ForeignKeyOrFreeText(
        omodels.Clinical_advice_reason_for_interaction
    )
    clinical_discussion = models.TextField(blank=True)
    agreed_plan = models.TextField(blank=True)
    discussed_with = models.CharField(max_length=255, blank=True)
    clinical_advice_given = models.NullBooleanField()
    infection_control_advice_given = models.NullBooleanField()
    change_in_antibiotic_prescription = models.NullBooleanField()
    referred_to_opat = models.NullBooleanField()

    def set_reason_for_interaction(self, incoming_value, user, data):
        if(incoming_value in MICROHAEM_CONSULTATIONS):
            episode = Episode.objects.get(pk=data["episode_id"])
            exists = Tagging.objects.filter(
                episode=episode, team__name=MICROHAEM_TEAM_NAME
            )
            exists = exists.exists()
            if not exists:
                Tagging.objects.create(
                    episode=episode,
                    team=Team.objects.get(name=MICROHAEM_TEAM_NAME)
                )
        self.reason_for_interaction = incoming_value


class Todo(EpisodeSubrecord):
    _title = 'To Do'
    _icon = 'fa fa-th-list'

    details = models.TextField(blank=True)

class Hiv_no(lookuplists.LookupList):
    class Meta:
        verbose_name = "HIV refusal reason"


class MicrobiologyTest(EpisodeSubrecord):
    _title = 'Investigations'
    _sort = 'date_ordered'
    _icon = 'fa fa-crosshairs'
    _modal = 'lg'

    test                  = models.CharField(max_length=255)
    alert_investigation   = models.BooleanField(default=False)
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
    hiv_declined          = ForeignKeyOrFreeText(Hiv_no)

"""
Begin OPAT specific fields.
"""

class Unplanned_stop(lookuplists.LookupList):
    class Meta:
        verbose_name = "Unplanned stop"


class Opat_rvt(lookuplists.LookupList):
    class Meta:
        verbose_name = "OPAT RVT"


class OPATMeta(EpisodeSubrecord):
    review_date           = models.DateField(blank=True, null=True)
    reason_for_stopping   = models.CharField(max_length=200, blank=True, null=True)
    unplanned_stop_reason = ForeignKeyOrFreeText(Unplanned_stop)
    stopping_iv_details   = models.CharField(max_length=200, blank=True, null=True)
    treatment_outcome     = models.CharField(max_length=200, blank=True, null=True)
    deceased              = models.NullBooleanField(default=False)
    death_category        = models.CharField(max_length=200, blank=True, null=True)
    cause_of_death        = models.CharField(max_length=200, blank=True, null=True)
    readmitted            = models.NullBooleanField(default=False)
    readmission_cause     = models.CharField(max_length=200, blank=True, null=True)
    notes                 = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "OPAT meta"


class OPATOutcome(EpisodeSubrecord):
    """
    This captures the final data for an OAPT episode - it is much the
    same as OPAT meta data, but captured on the ward round and interrogated
    differently.
    """
    _is_singleton     = True
    _title            = "OPAT Outcome"

    treatment_outcome     = models.CharField(max_length=200, blank=True, null=True)
    deceased              = models.NullBooleanField(default=False)
    death_category        = models.CharField(max_length=200, blank=True, null=True)
    cause_of_death        = models.CharField(max_length=200, blank=True, null=True)
    readmitted            = models.NullBooleanField(default=False)
    readmission_cause     = models.CharField(max_length=200, blank=True, null=True)
    notes                 = models.TextField(blank=True, null=True)
    patient_feedback      = models.NullBooleanField(default=False)

    class Meta:
        verbose_name = "OPAT outcome"


class OPATRejection(EpisodeSubrecord):

    decided_by            = models.CharField(max_length=255, blank=True, null=True)
    patient_choice        = models.NullBooleanField(default=False)
    oral_available        = models.NullBooleanField(default=False)
    not_needed            = models.NullBooleanField(default=False)
    patient_suitability   = models.NullBooleanField(default=False)
    not_fit_for_discharge = models.NullBooleanField(default=False)
    non_complex_infection = models.NullBooleanField(default=False)
    no_social_support     = models.NullBooleanField(default=False)
    reason                = models.CharField(max_length=255, blank=True, null=True)
    date                  = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "OPAT rejection"


class Line(EpisodeSubrecord):
    _sort = 'insertion_datetime'
    _icon = 'fa fa-bolt'

    line_type            = ForeignKeyOrFreeText(omodels.Line_type)
    site                 = ForeignKeyOrFreeText(omodels.Line_site)
    insertion_datetime   = models.DateTimeField(blank=True, null=True)
    inserted_by          = models.CharField(max_length=255, blank=True, null=True)
    external_length      = models.CharField(max_length=255, blank=True, null=True)
    removal_datetime     = models.DateTimeField(blank=True, null=True)
    complications        = ForeignKeyOrFreeText(omodels.Line_complication)
    removal_reason       = ForeignKeyOrFreeText(omodels.Line_removal_reason)
    special_instructions = models.TextField()


class OPATReview(EpisodeSubrecord):
    _sort = 'datetime'
    _title = 'OPAT Review'
    _icon = 'fa fa-comments'
    _list_limit = 1
    _modal = 'lg'

    datetime                = models.DateTimeField(null=True, blank=True)
    initials                = models.CharField(max_length=255, blank=True)
    rv_type                 = ForeignKeyOrFreeText(Opat_rvt)
    discussion              = models.TextField(blank=True, null=True)
    opat_plan               = models.TextField(blank=True)
    next_review             = models.DateField(blank=True, null=True)
    dressing_changed        = models.NullBooleanField(default=False)
    bung_changed            = models.NullBooleanField(default=False)
    medication_administered = models.TextField(blank=True, null=True)
    adverse_events          = ForeignKeyOrFreeText(omodels.Antimicrobial_adverse_event)

    class Meta:
        verbose_name = "OPAT review"


class OPATOutstandingIssues(EpisodeSubrecord):
    _title = 'Outstanding Issues'
    _icon = 'fa fa-th-list'
    _advanced_searchable = False

    details = models.TextField(blank=True)

    class Meta:
        verbose_name = "OPAT outstanding issue"


class Appointment(EpisodeSubrecord):
    _title = 'Upcoming Appointments'
    _sort = 'date'
    _icon = 'fa fa-calendar'
    _advanced_searchable = False

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
    dressing_intact        = models.NullBooleanField(default=False)
    lumen_flush_ok         = models.NullBooleanField(default=False)
    blood_drawback_seen    = models.NullBooleanField(default=False)
    cm_from_exit_site      = models.NullBooleanField(default=False)

    class Meta:
        verbose_name = "OPAT line assessment"


"""
Fields for UCLH - specific Research studies.
"""

""" RiD RTI (http://www.rid-rti.eu/ ) """
class Specimin(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Specimen"

class Organism_details(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name_plural = "Organism details"


class Checkpoints_assay(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Checkpoints assay values"
        verbose_name_plural = "Checkpoints assay values"


class Antimicrobial_susceptability(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Antimicrobial susceptability"
        verbose_name_plural = "Antimicrobial susceptibilities"


class Specimin_appearance(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Specimen appearance"


class LabSpecimin(EpisodeSubrecord):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Lab specimen appearance"

    _title = 'Lab Specimen'
    _sort = 'date_collected'
    _icon = 'fa fa-flask'

    specimin_type     = ForeignKeyOrFreeText(Specimin)
    date_collected    = models.DateField(blank=True, null=True)
    volume            = models.CharField(max_length=200, blank=True, null=True)
    appearance        = ForeignKeyOrFreeText(Specimin_appearance)
    epithelial_cell   = models.CharField(max_length=200, blank=True, null=True)
    white_blood_cells = models.CharField(max_length=200, blank=True, null=True)
    date_tested       = models.DateField(blank=True, null=True)
    external_id       = models.CharField(max_length=200, blank=True, null=True)
    biobanking        = models.NullBooleanField(default=False)
    biobanking_box    = models.CharField(max_length=200, blank=True, null=True)
    date_biobanked    = models.DateField(blank=True, null=True)
    volume_biobanked  = models.CharField(max_length=200, blank=True, null=True)


# This is based on the investigations record type from elCID
class LabTest(EpisodeSubrecord):
    _sort = 'date_ordered'
    _icon = 'fa fa-crosshairs'
    _advanced_searchable = False

    test                         = models.CharField(max_length=255)
    date_ordered                 = models.DateField(null=True, blank=True)
    details                      = models.CharField(max_length=255, blank=True)
    result                       = models.CharField(max_length=255, blank=True)
    significant_organism         = models.NullBooleanField(default=False)
    organism_details             = ForeignKeyOrFreeText(Organism_details)
    antimicrobials_susceptible   = ForeignKeyOrFreeText(Antimicrobial_susceptability,
                                                        related_name='susceptible')
    antimicrobials_intermediate  = ForeignKeyOrFreeText(Antimicrobial_susceptability,
                                                        related_name='intermediate')
    antimicrobials_resistant     = ForeignKeyOrFreeText(Antimicrobial_susceptability,
                                                        related_name='resistant')
    retrieved                    = models.NullBooleanField(default=False)
    date_retrieved               = models.DateField(null=True, blank=True)
    sweep_biobanked              = models.NullBooleanField(default=False)
    organism_biobanked           = models.NullBooleanField(default=False)
    freezer_box_number           = models.CharField(max_length=200, blank=True, null=True)
    esbl                         = models.NullBooleanField(default=False)
    carbapenemase                = models.NullBooleanField(default=False)


class RidRTITest(EpisodeSubrecord):
    """
    Results of the actual RiD RTI test !
    """
    _advanced_searchable = False

    test            = models.CharField(max_length=200, blank=True, null=True)
    notes           = models.TextField(blank=True, null=True)
    # HAP/VAP results
    pseudomonas_aeruginosa = models.NullBooleanField(default=False)
    acinetobacter_baumannii = models.NullBooleanField(default=False)
    senotophomonas_maltophilia = models.NullBooleanField(default=False)
    klebsiella_spp = models.NullBooleanField(default=False)
    enterobacter_spp = models.NullBooleanField(default=False)
    staphylococcus_aureus = models.NullBooleanField(default=False)
    staphylococcus_mrsa = models.NullBooleanField(default=False)
    ctx_m = models.NullBooleanField(default=False)
    shv_esbl = models.NullBooleanField(default=False)
    tem_esbl = models.NullBooleanField(default=False)
    vim = models.NullBooleanField(default=False)
    imp = models.NullBooleanField(default=False)
    ndm = models.NullBooleanField(default=False)
    kpc = models.NullBooleanField(default=False)
    oxa_48 = models.NullBooleanField(default=False)
    meca = models.NullBooleanField(default=False)
    # CAP results
    mycoplasma_pneumoniae = models.NullBooleanField(default=False)
    chlamydophila_pneumoniae = models.NullBooleanField(default=False)
    legionella_pneumophila = models.NullBooleanField(default=False)
    # (Mycobacterium tuberculosis complex) = models.NullBooleanField(default=False)
    mtc = models.NullBooleanField(default=False)
    haemophilus_influenzae = models.NullBooleanField(default=False)
    streptococcus_pneumoniae = models.NullBooleanField(default=False)
    rsva = models.NullBooleanField(default=False)
    rsvb = models.NullBooleanField(default=False)
    influenza_a = models.NullBooleanField(default=False)
    influenza_b      = models.NullBooleanField(default=False)
    cap_coronavirus_oc43 = models.NullBooleanField(default=False)
    cap_coronavirus_hku1 = models.NullBooleanField(default=False)
    cap_coronavirus_nl63 = models.NullBooleanField(default=False)
    cap_coronavirus_229e = models.NullBooleanField(default=False)
    # ORTI results
    nocardia_spp = models.NullBooleanField(default=False)
    rhodococcus_equi = models.NullBooleanField(default=False)
    # (Aspergillus spp Cryptococcus neoformans)
    aspergillus_spp = models.NullBooleanField(default=False)
    cryptococcus_neoformans = models.NullBooleanField(default=False)
    pneumocystis_jiroveci = models.NullBooleanField(default=False)
    orti_coronavirus_oc43 = models.NullBooleanField(default=False)
    orti_coronavirus_hku1 = models.NullBooleanField(default=False)
    orti_coronavirus_nl63 = models.NullBooleanField(default=False)
    orti_coronavirus_229e = models.NullBooleanField(default=False)

    class Meta:
        verbose_name = "RiD-RTI"

class CheckpointsAssay(EpisodeSubrecord):
    _is_singleton = True
    _advanced_searchable = False

    acc = models.NullBooleanField(default=False)
    act_mir = models.NullBooleanField(default=False)
    bel = models.NullBooleanField(default=False)
    cmy_i_mox = models.NullBooleanField(default=False)
    cmy_ii = models.NullBooleanField(default=False)
    ctx_m_1_group = models.NullBooleanField(default=False)
    ctx_m_1_like = models.NullBooleanField(default=False)
    ctx_m_15_like = models.NullBooleanField(default=False)
    ctx_m_2_group = models.NullBooleanField(default=False)
    ctx_m_3_like = models.NullBooleanField(default=False)
    ctx_m_32_like = models.NullBooleanField(default=False)
    ctx_m_8_25_group = models.NullBooleanField(default=False)
    ctx_m_9_group = models.NullBooleanField(default=False)
    dha = models.NullBooleanField(default=False)
    fox = models.NullBooleanField(default=False)
    ges = models.NullBooleanField(default=False)
    gim = models.NullBooleanField(default=False)
    imp = models.NullBooleanField(default=False)
    kpc = models.NullBooleanField(default=False)
    ndm = models.NullBooleanField(default=False)
    oxa_23_like = models.NullBooleanField(default=False)
    oxa_24_like = models.NullBooleanField(default=False)
    oxa_48_like = models.NullBooleanField(default=False)
    oxa_58_like = models.NullBooleanField(default=False)
    per = models.NullBooleanField(default=False)
    shv_e240k = models.NullBooleanField(default=False)
    shv_g238a = models.NullBooleanField(default=False)
    shv_g238s = models.NullBooleanField(default=False)
    shv_wt = models.NullBooleanField(default=False)
    spm = models.NullBooleanField(default=False)
    tem_e104k = models.NullBooleanField(default=False)
    tem_g238s = models.NullBooleanField(default=False)
    tem_r164c = models.NullBooleanField(default=False)
    tem_r164h = models.NullBooleanField(default=False)
    tem_r164s = models.NullBooleanField(default=False)
    tem_wt = models.NullBooleanField(default=False)
    veb = models.NullBooleanField(default=False)
    vim = models.NullBooleanField(default=False)

    negative = models.NullBooleanField(default=False)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Checkpoints assay"
