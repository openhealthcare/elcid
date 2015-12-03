from elcid.models import (
    Diagnosis, Line, Antimicrobial, BloodCulture, Location, PrimaryDiagnosis,
    Infection
)
from opal.models import Patient
from pathway.pathways import Pathway, Step


class BloodCulturePathway(Pathway):
    title = "Blood Culture"
    steps = (
        Step(
            template_url="/pathway/templates/find_patient_form.html",
            controller_class="FindPatientCtrl",
            title="Find Patient",
            icon="fa fa-user"
        ),
        Step(
            model=Location,
            controller_class="BloodCultureLocationCtrl",
            template_url="/templates/pathway/blood_culture_location.html"
        ),
        PrimaryDiagnosis,
        Diagnosis,
        Infection,
        Step(
            model=Line,
            template_url="/pathway/templates/optional_line.html",
            controller_class="LineController"
        ),
        Antimicrobial,
    )

    def save(self, data, user):
        update_demographics = data["demographics"]
        hospital_number = update_demographics["hospital_number"]
        patient, created = Patient.objects.get_or_create(
            demographics__hospital_number=hospital_number
        )

        if created:
            demographics_model = patient.demographics_set.first()
            for k, v in update_demographics.iteritems():
                setattr(demographics_model, k, v)
            demographics_model.save()

        if not patient.episode_set.exists():
            episode = patient.create_episode()
        else:
            episode = patient.episode_set.last()

        tagging = data["tagging"]
        episode.set_tag_names(tagging, user)

        for step in self.get_steps():
            step.save(episode.id, data, user)

        return episode
