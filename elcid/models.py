"""
elCID implementation specific models!
"""
from django.db import models

import opal.models as omodels

from opal.models import (
    EpisodeSubrecord, PatientSubrecord, Episode, Team,
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
    _icon = 'fa fa-users'

    gp    = models.TextField(blank=True, null=True)
    nurse = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Carers"


class DuplicatePatient(PatientSubrecord):
    _no_admin = True
    _icon = 'fa fa-clone'
    _advanced_searchable = False
    reviewed = models.BooleanField(default=False)
    merged = models.BooleanField(default=False)

    def icon(self):
        return self._icon


class Location(EpisodeSubrecord):
    _is_singleton = True
    _icon = 'fa fa-map-marker'

    category                   = models.CharField(max_length=255, blank=True)
    hospital                   = models.CharField(max_length=255, blank=True)
    ward                       = models.CharField(max_length=255, blank=True)
    bed                        = models.CharField(max_length=255, blank=True)
    # This is completely the wrong place for these - they need to go in their
    # own OPATReferral model. The ticket for that work is currently
    # opal-ideas#21
    opat_referral_route        = models.CharField(max_length=255, blank=True,
                                                  null=True)
    opat_referral_team         = models.CharField(max_length=255, blank=True,
                                                  null=True)
    opat_referral_consultant   = models.CharField(max_length=255, blank=True,
                                                  null=True)
    opat_referral_team_address = models.TextField(blank=True, null=True)
    opat_referral              = models.DateField(blank=True, null=True)
    opat_acceptance            = models.DateField(blank=True, null=True)
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

    symptom = ForeignKeyOrFreeText(omodels.Symptom)
    symptoms = models.ManyToManyField(omodels.Symptom, related_name="presenting_complaints")
    duration = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def set_symptom(self, *args, **kwargs):
        # ignore symptom for the time being
        pass

    def to_dict(self, user):
        return dict(
            symptoms=[i.name for i in self.symptoms.all()],
            duration=self.duration,
            details=self.details
        )

    @classmethod
    def _get_fieldnames_to_serialize(cls):
        field_names = super(PresentingComplaint, cls)._get_fieldnames_to_serialize()
        removed_fields = {u'symptom_fk_id', 'symptom_ft', 'symptom'}
        field_names = [i for i in field_names if i not in removed_fields]
        return field_names


class PrimaryDiagnosis(EpisodeSubrecord):
    """
    This is the confirmed primary diagnosisa
    """
    _is_singleton = True
    _title = 'Primary Diagnosis'

    condition = ForeignKeyOrFreeText(omodels.Condition)
    confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Primary diagnoses"


class Consultant(lookuplists.LookupList):
    pass

class ConsultantAtDischarge(EpisodeSubrecord):
    _title = 'Consultant At Discharge'
    _is_singleton = True
    consultant = ForeignKeyOrFreeText(Consultant)


class SecondaryDiagnosis(EpisodeSubrecord):
    """
    This is a confirmed diagnosis at discharge time.
    """
    _title = 'Secondary Diagnosis'
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
    no_antimicrobials = models.NullBooleanField(default=False)


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
            if self.id:
                episode = self.episode
            else:
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
    spotted_fever_igm     = models.CharField(max_length=20, blank=True)
    spotted_fever_igg     = models.CharField(max_length=20, blank=True)
    typhus_group_igm      = models.CharField(max_length=20, blank=True)
    typhus_group_igg      = models.CharField(max_length=20, blank=True)
    scrub_typhus_igm      = models.CharField(max_length=20, blank=True)
    scrub_typhus_igg      = models.CharField(max_length=20, blank=True)


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

class Appointment(EpisodeSubrecord):
    _title = 'Upcoming Appointments'
    _sort = 'date'
    _icon = 'fa fa-calendar'
    _advanced_searchable = False

    appointment_type = models.CharField(max_length=200, blank=True, null=True)
    appointment_with = models.CharField(max_length=200, blank=True, null=True)
    date             = models.DateField(blank=True, null=True)
