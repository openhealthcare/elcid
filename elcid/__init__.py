"""
elCID OPAL implementation
"""

from opal.core import application, menus

from microhaem.constants import MICROHAEM_ROLE
from django.core.urlresolvers import reverse



class Application(application.OpalApplication):
    schema_module = 'elcid.schema'
    javascripts = [
        'js/elcid/routes.js',
        'js/elcid/controllers/discharge.js',
        'js/elcid/controllers/confirm_discharge.js',
        'js/elcid/controllers/diagnosis_hospital_number.js',
        'js/elcid/controllers/diagnosis_add_episode.js',
        'js/elcid/controllers/diagnosis_discharge.js',
        'js/elcid/controllers/clinical_advice_form.js',
        'js/elcid/controllers/haem_view.js',
        'js/elcid/controllers/result_view.js',
        'js/elcid/services/dicharge_patient.js',
        'js/elcid/services/flow.js',
        'js/elcid/services/location_ward_comparator.js',
        'js/elcid/services/records/investigation.js',
        'js/elcid/services/records/general_note.js',
        'js/elcid/services/records/diagnosis.js',
        'js/elcid/services/records/microbiology_input.js',
        'js/elcid/services/records/line.js',
        'js/elcid/services/records/opat_line_assessment.js',
        'js/elcid/services/records/opat_review.js',
        'js/elcid/services/records/antimicrobial.js',
    ]

    styles = [
        "css/infectiousdiseases.css"
    ]

    actions = [
        'actions/presenting_complaint.html',
    ]

    patient_view_forms = {
        "General Consultation": "inline_forms/clinical_advice.html",
    }

    @classmethod
    def get_menu_items(klass, user=None):

        if user:
            if not user.is_authenticated():
                return [menus.MenuItem(
                    href=reverse('login'),
                    icon='fa-sign-in',
                    display='Log In')
                ]

        # import pathways here as this being in the init
        # causes issues with django settings in heroku otherwise
        items = application.OpalApplication.get_menu_items(user=user)
        if user.profile.can_extract or user.is_superuser:
            query = menus.MenuItem(
                href="/search/#/extract/",
                activepattern="/search/#/extract",
                icon="fa-download",
                display="Extract"
            )
            items.append(query)

        menuitem = menus.MenuItem(
            href='/referrals/',
            display="Referrals",
            icon="fa fa-mail-forward",
            activepattern='referrals',
            index=3
        )

        items.append(menuitem)

        return items
