from opal.models import EpisodeSubrecord
from django.db import models


class ExternalLiasonContactDetails(EpisodeSubrecord):
    # required
    external_hospital_number = models.CharField(
        max_length=256,
    )

    # required
    hospital = models.CharField(
        max_length=256
    )

    hospital_contact = models.CharField(
        max_length=256
    )

    contact_telephone_number = models.CharField(
        max_length=256
    )

    # not using an email field because at the
    # moment validation won't flow through
    contact_email_address = models.CharField(
        max_length=256
    )
