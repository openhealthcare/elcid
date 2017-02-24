"""
elCID OPAL implementation
"""

from opal.core import application


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
        'js/elcid/services/records/investigation.js',
        'js/elcid/services/records/general_note.js',
        'js/elcid/services/records/diagnosis.js',
        'js/elcid/services/records/microbiology_input.js',
        'js/elcid/services/records/line.js',
        'js/elcid/services/records/opat_line_assessment.js',
        'js/elcid/services/records/opat_review.js',
        'js/elcid/services/records/antimicrobial.js',
    ]

    actions = [
        'actions/presenting_complaint.html',
        'actions/mine.html'
    ]

    patient_view_forms = {
        "General Consultation": "inline_forms/clinical_advice.html",
    }
