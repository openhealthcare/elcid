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
