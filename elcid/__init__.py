"""
elCID Royal Free Hospital implementation
"""

from opal.core import application


class Application(application.OpalApplication):
    schema_module = 'elcid.schema'
    flow_module = 'elcid.flow'
    javascripts = [
        'js/elcid/routes.js',
        'js/elcid/controllers/discharge.js',
        'js/elcid/controllers/diagnosis_hospital_number.js',
        'js/elcid/controllers/diagnosis_add_episode.js',
        'js/elcid/controllers/diagnosis_discharge.js',
        'js/elcid/controllers/patient_notes.js',
        'js/elcid/controllers/micro_haem_discussion_form.js',
        'js/elcid/controllers/clinical_advice_form.js',
        'js/elcid/controllers/welcome.js',
        'js/elcid/controllers/procedure_form.js',
        'js/elcid/controllers/blood_culture_location.js',
        'js/elcid/services/dicharge_patient.js',
    ]

    actions = [
        'actions/presenting_complaint.html'
    ]

    patient_view_forms = {
        "General Consultation": "inline_forms/clinical_advice.html",
    }

    menuitems = [
        dict(
            href='/pathway/#/add_patient', display='Add Patient', icon='fa fa-plus',
            activepattern='/pathway/#/add_patient')
    ]
