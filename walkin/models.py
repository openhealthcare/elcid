"""
Models for the OPAL Walkin clinic plugin
"""
from django.db import models

from opal import models as omodels
from opal.core import lookuplists
from opal.core.fields import ForeignKeyOrFreeText

class Management_follow_up(lookuplists.LookupList):
    class Meta:
        verbose_name = "Management follow up"


class Management_clinics(lookuplists.LookupList):
    class Meta:
        verbose_name = "Management clinics"
        verbose_name_plural = "Management clinics"


class Wi_nurse_reason(lookuplists.LookupList):
    class Meta:
        verbose_name = "Walkin nurse reason"


class Findings_rash_type(lookuplists.LookupList):
    class Meta:
        verbose_name = "Findings rash type"


class Findings_rash_distribution(lookuplists.LookupList):
    class Meta:
        verbose_name = "Findings rash distribution"


class Symptom(omodels.EpisodeSubrecord):
    _title = 'Symptoms'
    _icon = 'fa fa-stethoscope'
    HELP_DURATION = "The duration for which the patient had been experiencing \
these symptoms when recorded."

    symptoms = models.ManyToManyField(
        omodels.Symptom, related_name="walkin_symptoms"
    )
    duration = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=HELP_DURATION
    )
    details = models.TextField(blank=True, null=True)

    # deprecated fields 9/11/2015
    onset = models.CharField(max_length=255, blank=True, null=True)
    symptom = ForeignKeyOrFreeText(omodels.Symptom)

    @classmethod
    def _get_fieldnames_to_serialize(cls):
        field_names = super(Symptom, cls)._get_fieldnames_to_serialize()
        removed_fields = {u'symptom_fk_id', 'symptom_ft', 'symptom', 'onset'}
        field_names = [i for i in field_names if i not in removed_fields]
        return field_names

    def set_symptom(self, *args, **kwargs):
        # ignore symptom for the time being
        pass


class ClinicalFindings(omodels.EpisodeSubrecord):
    _title        = 'Clinical Findings'
    _icon         = 'fa fa-stethoscope'

    lymphadenopathy         = models.CharField(
        max_length=20, blank=True, null=True
    )
    lymphadenopathy_details = models.CharField(
        max_length=255, blank=True, null=True
    )
    jaundice                = models.CharField(max_length=20, blank=True)
    dehydrated              = models.CharField(max_length=20, blank=True)

    rash                    = models.CharField(max_length=20, blank=True)
    rash_type               = ForeignKeyOrFreeText(Findings_rash_type)
    rash_distribution       = ForeignKeyOrFreeText(Findings_rash_distribution)

    cardiovascular          = models.CharField(
        max_length=255, blank=True, null=True
    )

    respiratory             = models.CharField(
        max_length=255, blank=True, null=True
    )
    abdominal               = models.CharField(
        max_length=255, blank=True, null=True
    )
    oropharnyx              = models.CharField(
        max_length=255, blank=True, null=True
    )
    neurological            = models.CharField(
        max_length=255, blank=True, null=True
    )
    other_findings          = models.CharField(
        max_length=255, blank=True, null=True
    )


class Management(omodels.EpisodeSubrecord):
    _is_singleton = True
    _icon = 'fa fa-list-ol'
    _title = 'Walkin Management'

    follow_up           = ForeignKeyOrFreeText(Management_follow_up)
    follow_up_clinic    = ForeignKeyOrFreeText(Management_clinics)
    date_of_appointment = models.DateField(null=True, blank=True)
    advice              = models.CharField(
        max_length=255, blank=True, null=True
    )
    results_actioned    = models.CharField(
        max_length=255, blank=True, null=True
    )

    def __unicode__(self):
        return u'Management: {0}'.format(self.id)


class WalkinNurseLedCare(omodels.EpisodeSubrecord):
    _icon  = 'fa fa-user-md'
    _title = 'Nurse led care'

    reason    = ForeignKeyOrFreeText(Wi_nurse_reason)
    treatment = models.TextField(blank=True, null=True)


class ZikaPathway(omodels.EpisodeSubrecord):
    _icon = 'fa fa-warning'
    _advanced_searchable = False

    pregnant           = models.BooleanField(default=False)
    gestation          = models.CharField(max_length=255, blank=True, null=True)
    due_date           = models.DateField(blank=True, null=True)
    antenatal_hospital = models.CharField(max_length=255, blank=True, null=True)
    yellow_fever       = models.CharField(max_length=255, blank=True, null=True)
    date_leaving       = models.DateField(blank=True, null=True)
    advice             = models.TextField(blank=True, null=True)
    follow_up          = models.TextField(blank=True, null=True)
