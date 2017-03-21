"""
Models for opat
"""
from django.db import models
from opal.core import lookuplists
from opal.models import EpisodeSubrecord
import opal.models as omodels
from opal.core.fields import ForeignKeyOrFreeText


class OPATInfectiveDiagnosis(lookuplists.LookupList):
    pass


class OPATDressingType(lookuplists.LookupList):
    pass


class Opat_rvt(lookuplists.LookupList):
    class Meta:
        verbose_name = "OPAT RVT"


class Unplanned_stop(lookuplists.LookupList):
    class Meta:
        verbose_name = "Unplanned stop"


class OPATReview(EpisodeSubrecord):
    _sort = 'datetime'
    _title = 'OPAT Review'
    _icon = 'fa fa-comments'
    _list_limit = 1
    _angular_service = 'OPATReview'

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


class OPATLineAssessment(EpisodeSubrecord):
    _title = 'OPAT Line Assessment'
    _icon = 'fa fa-check-square-o'
    _angular_service = 'OPATLineAssessment'

    line                   = models.CharField(max_length=200, blank=True, null=True)
    assessment_date        = models.DateField(blank=True, null=True)
    vip_score              = models.IntegerField(blank=True, null=True)
    dressing_type          = models.CharField(max_length=200, blank=True, null=True)
    dressing_change_date   = models.DateField(blank=True, null=True)
    dressing_change_reason = models.CharField(max_length=200, blank=True, null=True)
    next_bionector_date    = models.DateField(blank=True, null=True)
    bionector_change_date  = models.DateField(blank=True, null=True)
    comments               = models.TextField(blank=True, null=True)
    dressing_intact        = models.NullBooleanField(default=False)
    lumen_flush_ok         = models.NullBooleanField(default=False)
    blood_drawback_seen    = models.NullBooleanField(default=False)
    cm_from_exit_site      = models.FloatField(default=False)

    class Meta:
        verbose_name = "OPAT line assessment"

class OPATMeta(EpisodeSubrecord):
    _clonable = False
    _title = "OPAT Episode"

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
        verbose_name = "OPAT episode"


class OPATOutcome(EpisodeSubrecord):
    """
    This captures the final data for an OAPT episode - it is much the
    same as OPAT meta data, but captured on the ward round and interrogated
    differently.
    """
    _title            = "OPAT Outcome"
    _clonable         = False

    outcome_stage         = models.CharField(max_length=200, blank=True, null=True)
    treatment_outcome     = models.CharField(max_length=200, blank=True, null=True)
    patient_outcome       = models.CharField(max_length=200, blank=True, null=True)
    opat_outcome          = models.CharField(max_length=200, blank=True, null=True)
    deceased              = models.NullBooleanField(default=False)
    death_category        = models.CharField(max_length=200, blank=True, null=True)
    cause_of_death        = models.CharField(max_length=200, blank=True, null=True)
    readmitted            = models.NullBooleanField(default=False)
    readmission_cause     = models.CharField(max_length=200, blank=True, null=True)
    notes                 = models.TextField(blank=True, null=True)
    patient_feedback      = models.NullBooleanField(default=False)
    infective_diagnosis   = ForeignKeyOrFreeText(OPATInfectiveDiagnosis)

    class Meta:
        verbose_name = "OPAT outcome"


class OPATRejection(EpisodeSubrecord):
    _clonable = False

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
