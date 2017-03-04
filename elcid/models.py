"""
elCID implementation specific models!
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from jsonfield import JSONField

import opal.models as omodels

from opal.models import (
    EpisodeSubrecord, PatientSubrecord, Episode,
    Tagging, ExternallySourcedModel
)
from opal.core.fields import ForeignKeyOrFreeText
from opal.core import lookuplists
from microhaem.constants import MICROHAEM_CONSULTATIONS, MICROHAEM_TAG


class Demographics(omodels.Demographics, omodels.ExternallySourcedModel):
    _is_singleton = True
    _icon = 'fa fa-user'

    pid_fields       = (
        'hospital_number', 'nhs_number', 'surname', 'first_name',
        'middle_name', 'post_code',
    )

    class Meta:
        verbose_name_plural = "Demographics"

    @classmethod
    def get_form_template(cls, patient_list=None, episode_type=None):
        if settings.GLOSS_ENABLED:
            return super(Demographics, cls).get_form_template(patient_list=None, episode_type=None)
        else:
            return "forms/demographics_form_pre_gloss.html"


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


class Location(omodels.Location):
    # This is completely the wrong place for these - they need to go in their
    # own OPATReferral model. The ticket for that work is currently
    # opal-ideas#21
    opat_referral_route        = models.CharField(max_length=255, blank=True,
                                                  null=True)
    opat_referral_team         = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Referring Team"
    )
    opat_referral_consultant   = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Referring Consultant"
    )
    opat_referral_team_address = models.TextField(
        blank=True, null=True, verbose_name="Referring team address"
    )
    opat_referral              = models.DateField(blank=True, null=True, verbose_name="Date Of Referral To OPAT")
    opat_acceptance            = models.DateField(blank=True, null=True, verbose_name="Referring Consultant")
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


class Result(PatientSubrecord):
    _icon = 'fa fa-crosshairs'

    lab_number = models.CharField(max_length=255, blank=True, null=True)
    profile_code = models.CharField(max_length=255, blank=True, null=True)
    external_identifier = models.CharField(max_length=255, blank=True, null=True)
    profile_description = models.CharField(max_length=255, blank=True, null=True)
    request_datetime = models.DateTimeField(blank=True, null=True)
    observation_datetime = models.DateTimeField(blank=True, null=True)
    last_edited = models.DateTimeField(blank=True, null=True)
    result_status = models.CharField(max_length=255, blank=True, null=True)
    observations = JSONField(blank=True, null=True)

    def update_from_dict(self, data, *args, **kwargs):
        if "id" not in data:
            if "patient_id" not in data:
                raise ValueError("no patient id found for result in %s" % data)
            if "external_identifier" in data and data["external_identifier"]:
                existing = Result.objects.filter(
                    external_identifier=data["external_identifier"],
                    patient=data["patient_id"]
                ).first()

                if existing:
                    data["id"] = existing.id

        super(Result, self).update_from_dict(data, *args, **kwargs)


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
        field_names = self.__class__._get_fieldnames_to_serialize()
        result = {
            i: getattr(self, i) for i in field_names if not i == "symptoms"
        }
        result["symptoms"] = list(self.symptoms.values_list("name", flat=True))
        return result

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


class Diagnosis(omodels.Diagnosis):
    """
    This is a working-diagnosis list, will often contain things that are
    not technically diagnoses, but is for historical reasons, called diagnosis.
    """
    _angular_service = 'Diagnosis'

    def __unicode__(self):
        return u'Diagnosis of {0} - {1}'.format(
            self.condition,
            self.date_of_diagnosis
            )

    class Meta:
        verbose_name_plural = "Diagnoses"


class PastMedicalHistory(omodels.PastMedicalHistory):
    pass


class GeneralNote(EpisodeSubrecord):
    _title = 'General Notes'
    _sort  = 'date'
    _icon = 'fa fa-info-circle'
    _angular_service = 'GeneralNote'

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
    _angular_service = 'Antimicrobial'

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


class Allergies(omodels.Allergies, ExternallySourcedModel):
    # previously called drug this is the name of the problematic substance
    allergy_description = models.CharField(max_length=255, blank=True)
    allergy_type_description = models.CharField(max_length=255, blank=True)
    certainty_id = models.CharField(max_length=255, blank=True)
    certainty_description = models.CharField(max_length=255, blank=True)
    allergy_reference_name = models.CharField(max_length=255, blank=True)
    allergen_reference_system = models.CharField(max_length=255, blank=True)
    allergen_reference = models.CharField(max_length=255, blank=True)
    status_id = models.CharField(max_length=255, blank=True)
    status_description = models.CharField(max_length=255, blank=True)
    diagnosis_datetime = models.DateTimeField(null=True, blank=True)
    allergy_start_datetime = models.DateTimeField(null=True, blank=True)
    no_allergies = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Allergies"


class MicrobiologyInput(EpisodeSubrecord):
    _title = 'Clinical Advice'
    _sort = 'when'
    _icon = 'fa fa-comments'
    _list_limit = 3
    _angular_service = 'MicrobiologyInput'

    when = models.DateTimeField(null=True, blank=True)
    initials = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Advice given by"
    )
    reason_for_interaction = ForeignKeyOrFreeText(
        omodels.Clinical_advice_reason_for_interaction,
        verbose_name="Reason for clinical interaction"
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

            existing = Tagging.objects.filter(
                episode=episode, value=MICROHAEM_TAG
            )

            if existing.exists():
                existing.update(archived=False)
            else:
                Tagging.objects.create(
                    episode=episode,
                    value=MICROHAEM_TAG
                )
        self.reason_for_interaction = incoming_value


class Todo(EpisodeSubrecord):
    _title = 'To Do'
    _icon = 'fa fa-th-list'

    details = models.TextField(blank=True)

class Hiv_no(lookuplists.LookupList):
    class Meta:
        verbose_name = "HIV refusal reason"


class MicrobiologyTest(omodels.Investigation):
    _title = 'Investigations'
    _sort = 'date_ordered'
    _icon = 'fa fa-crosshairs'
    _angular_service = 'Investigation'

    alert_investigation   = models.BooleanField(default=False)
    hiv_declined          = ForeignKeyOrFreeText(
        Hiv_no, verbose_name="Reason not done"
    )
    spotted_fever_igm     = models.CharField(
        max_length=20, blank=True, verbose_name="Spotted Fever Group IgM"
    )
    spotted_fever_igg     = models.CharField(
        max_length=20, blank=True, verbose_name="Spotted Fever Group IgG"
    )
    typhus_group_igm      = models.CharField(
        max_length=20, blank=True, verbose_name="Typhus Group IgM"
    )
    typhus_group_igg      = models.CharField(
        max_length=20, blank=True, verbose_name="Typhus Group IgG"
    )
    scrub_typhus_igm      = models.CharField(
        max_length=20, blank=True, verbose_name="Scrub Typhus IgM"
    )
    scrub_typhus_igg      = models.CharField(
        max_length=20, blank=True, verbose_name="Scrub Typhus IgG"
    )


class Line(EpisodeSubrecord):
    _sort = 'insertion_datetime'
    _icon = 'fa fa-bolt'
    _angular_service = 'Line'

    line_type            = ForeignKeyOrFreeText(omodels.Line_type)
    site                 = ForeignKeyOrFreeText(omodels.Line_site)
    insertion_datetime   = models.DateTimeField(blank=True, null=True)
    inserted_by          = models.CharField(max_length=255, blank=True, null=True)
    external_length      = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="External Length When Inserted"
    )
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
    appointment_with = models.CharField(max_length=200, blank=True, null=True, verbose_name="With")
    date             = models.DateField(blank=True, null=True)


@receiver(post_save, sender=Episode)
def get_information_from_gloss(sender, **kwargs):
    from elcid import gloss_api

    episode = kwargs.pop("instance")
    created = kwargs.pop("created")
    if created and settings.GLOSS_ENABLED:
        hospital_number = episode.patient.demographics_set.first().hospital_number
        gloss_api.subscribe(hospital_number)
        gloss_api.patient_query(hospital_number, episode=episode)
