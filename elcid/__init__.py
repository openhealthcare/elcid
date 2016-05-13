"""
elCID OPAL implementation
"""

from opal.core import application


class Application(application.OpalApplication):
    schema_module = 'elcid.schema'
    javascripts = [
        'js/elcid/routes.js',
        'js/elcid/controllers/discharge.js',
        'js/elcid/controllers/diagnosis_hospital_number.js',
        'js/elcid/controllers/diagnosis_add_episode.js',
        'js/elcid/controllers/diagnosis_discharge.js',
        'js/elcid/controllers/clinical_advice_form.js',
        'js/elcid/controllers/haem_view.js',
        'js/elcid/controllers/result_view.js',
        'js/elcid/services/dicharge_patient.js',
        'js/elcid/services/flow.js',
    ]

    actions = [
        'actions/presenting_complaint.html'
    ]

    patient_view_forms = {
        "General Consultation": "inline_forms/clinical_advice.html",
    }
