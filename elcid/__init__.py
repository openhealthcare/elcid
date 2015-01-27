"""
elCID OPAL implementation
"""
from django.conf import settings

from opal import application

class Application(application.OpalApplication):
    schema_module = 'elcid.schema'
    flow_module   = 'elcid.flow'
