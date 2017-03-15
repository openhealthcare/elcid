from django.db import models

from opal.core.fields import ForeignKeyOrFreeText
from opal.core import lookuplists

from opal.models import PatientSubrecord


class HaemChemotherapyType(lookuplists.LookupList):
    class Meta:
        verbose_name = "Chemotherapy type"


class HaemTransplantType(lookuplists.LookupList):
    class Meta:
        verbose_name = "Transplant Type"


class HaemInformationType(lookuplists.LookupList):
    pass


class EpisodeOfNeutropenia(PatientSubrecord):
    _advanced_searchable = False
    _icon = 'fa fa-info-circle'
    _sort = 'start'
    _title = 'Episode of Neutropenia'
    start = models.DateField(blank=True, null=True)
    stop = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-start']

    @property
    def icon(self):
        return self._icon


class HaemInformation(PatientSubrecord):
    _icon = 'fa fa-info-circle'
    _title = 'Haematology Background Information'
    _advanced_searchable = False

    patient_type = ForeignKeyOrFreeText(HaemInformationType, verbose_name="Type")
    date_of_transplant = models.DateField(blank=True, null=True)
    neutropenia_onset = models.DateField(blank=True, null=True)
    type_of_transplant = ForeignKeyOrFreeText(HaemTransplantType, verbose_name="Transplant Type")
    type_of_chemotherapy = ForeignKeyOrFreeText(HaemChemotherapyType, verbose_name="Chemotherapy Type")
    date_of_chemotherapy = models.DateField(blank=True, null=True)
    count_recovery = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    @property
    def icon(self):
        return self._icon
