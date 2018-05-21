from django.core.management.base import BaseCommand
from elcid import models as emodels
from walkin import models as wmodels


class Command(BaseCommand):

    def handle(self, *args, **options):
        wsymptoms = wmodels.Symptom.objects.all()

        for wsymptom in wsymptoms:
            elcid_pc = emodels.PresentingComplaint.objects.create(
                created=wsymptom.created,
                updated=wsymptom.updated,
                created_by=wsymptom.created_by,
                updated_by=wsymptom.updated_by,
                consistency_token=wsymptom.consistency_token,
                details=wsymptom.details,
                duration=wsymptom.duration,
                onset=wsymptom.onset,
                episode_id=wsymptom.episode_id,
                symptom_fk_id=wsymptom.symptom_fk_id,
                symptom_ft=wsymptom.symptom_ft,
            )
            elcid_pc.symptoms.add(*wsymptom.symptoms.all())
