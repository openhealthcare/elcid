from opal.models import EpisodeSubrecord
from django.db import models


class ExternalLiaisonContactDetails(EpisodeSubrecord):
    _title = "Contact Details"
    _icon = 'fa fa-phone'
    _is_singleton = True
    _advanced_searchable = False

    # required
    external_hospital_number = models.CharField(
        max_length=256, null=True, blank=True
    )

    # required
    hospital = models.CharField(
        max_length=256, null=True, blank=True
    )

    hospital_contact = models.CharField(
        max_length=256, null=True, blank=True
    )

    contact_telephone_number = models.CharField(
        max_length=256, null=True, blank=True
    )

    # not using an email field because at the
    # moment validation won't flow through
    contact_email_address = models.CharField(
        max_length=256, null=True, blank=True
    )

    contact_notes = models.TextField(null=True, blank=True)


class LiaisonOutcome(EpisodeSubrecord):
    CLINIC_OPTIONS = (
        ("OPAT", "OPAT",),
        ("RAID", "RAID",),
        ("Walk-in", "Walk-in"),
    )

    LIAISON_STATE = (
        ("liaison ongoing", "liaison ongoing", ),
        ("end of liaison", "enf of liaison", ),
    )

    TRANSFER_OPTIONS = (
        ("Declined", "Declined",),
        ("Accepted", "Accepted",),
    )
    when = models.DateTimeField(null=True, blank=True)

    phone_advice_given = models.BooleanField(default=False)
    redirected_to_clinic = models.CharField(
        max_length=256, blank=True, null=True, choices=CLINIC_OPTIONS
    )

    email_advice_given = models.BooleanField(default=False)

    transfer_offered = models.BooleanField(default=False)
    transfer_response = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        choices=TRANSFER_OPTIONS
    )

    liaison_ended = models.NullBooleanField()
    next_date_of_contact = models.DateField(blank=True, null=True)
