from opal.core.pathway import WizardPathway, Step
from elcid.models import Diagnosis
from django.db import transaction
from microhaem.constants import MICROHAEM_TAG


class ReferPatientPathway(WizardPathway):
    display_name = "Haem Referral"
    slug = 'haem_referral'
    icon = "fa-mail-forward"

    steps = (
        Step(
            template="pathway/find_patient_form.html",
            step_controller="FindPatientCtrl",
            display_name="Find patient",
            icon="fa fa-user",
            base_template="pathways/base_steps/find_patient_with_help_text.html"
        ),
        Step(
            model=Diagnosis,
            base_template="pathways/base_steps/diagnosis.html",
            delete_others=False
        )
    )

    def redirect_url(self, user=None, patient=None, episode=None):
        return "/#/patient/{}/micro_haem".format(patient.id)

    @transaction.atomic
    def save(self, data, user=None, episode=None, patient=None):
        """
            Does 2 things.

            1. If an episode exists, for this patient, use the last one
            2. Tags the episode with Microhaem
        """
        if not episode:
            if patient:
                episode = patient.episode_set.last()

        patient, episode = super(ReferPatientPathway, self).save(
            data, user=user, episode=episode, patient=patient
        )

        tag_names = list(episode.get_tag_names(None))
        tag_names.append(MICROHAEM_TAG)
        episode.set_tag_names(tag_names, None)

        return patient, episode
