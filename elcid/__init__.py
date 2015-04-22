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
        'js/elcid/controllers/diagnosis_discharge.js'
    ]
    
    actions = [
        'actions/presenting_complaint.html'
    ]
