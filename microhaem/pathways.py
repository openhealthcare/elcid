from opal.core.pathway import WizardPathway, Step
from opal.utils import AbstractBase
from elcid.models import Diagnosis
from django.db import transaction
from microhaem import constants


class AbstractReferPatientPathway(WizardPathway, AbstractBase):
    display_name = "Haem Referral"
    icon = "fa-mail-forward"
    finish_button_text = "Add Patient"

    steps = (
        Step(
            template="unused",
            step_controller="UchFindPatientCtrl",
            display_name="Find patient",
            icon="fa fa-user",
            base_template="pathways/base_steps/find_patient_with_help_text.html"
        ),
        Step(
            model=Diagnosis,
            base_template="pathways/base_steps/diagnosis.html"
        ),
        Step(
            template="unused",
            display_name="Add to lists",
            icon="fa fa-tags",
            base_template="pathways/base_steps/add_to_teams.html"
        )
    )

    @transaction.atomic
    def save(self, data, user=None, episode=None, patient=None):
        """
            Tags the episode with the tag
        """
        tagging = data.pop("tagging", [])
        patient, episode = super(AbstractReferPatientPathway, self).save(
            data, user=user, episode=episode, patient=patient
        )
        tag_names = []
        if tagging:
            tag_names = [n for n, v in list(tagging[0].items()) if v]

        tag_names = list(episode.get_tag_names(None)) + tag_names
        tag_names.append(self.tag)
        episode.set_tag_names(tag_names, None)

        return patient, episode


class HaemReferalPathway(AbstractReferPatientPathway):
    display_name = "Haem Referral"
    slug = 'haem_referrals'
    tag = constants.MICROHAEM_TAG
    tag_display = "Micro Haematology"

    def redirect_url(self, user=None, patient=None, episode=None):
        return "/#/patient/{}/micro_haem".format(patient.id)


class OncologyReferalPathway(AbstractReferPatientPathway):
    display_name = "Oncology Referral"
    slug = 'oncology_referrals'
    tag = constants.ONCOLOGY_TAG
    tag_display = "Micro Oncology"


class MicroAdviceReferalPathway(AbstractReferPatientPathway):
    display_name = "Micro Advice Referral"
    slug = 'micro_advice_referrals'
    tag = constants.MICRO_ADVICE_TAG
    tag_display = "Micro advice"
