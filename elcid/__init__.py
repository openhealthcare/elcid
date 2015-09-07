"""
elCID OPAL implementation
"""
from django.conf import settings

from opal.core import application

class Application(application.OpalApplication):
    schema_module = 'elcid.schema'
    flow_module   = 'elcid.flow'
    javascripts   = [
        'js/elcid/routes.js',
        'js/elcid/controllers.js',
        'js/elcid/controllers/diagnosis_hospital_number.js',
        'js/elcid/controllers/diagnosis_add_episode.js',
        'js/elcid/controllers/diagnosis_discharge.js',
        'js/elcid/controllers/micro_haem_discussion_form.js'
    ]

    actions = [
        'actions/presenting_complaint.html'
    ]

    patient_view_forms = {
        "Micro Haem Round Discussion": "inline_forms/micro_haem_discussion_form.html"
    }
