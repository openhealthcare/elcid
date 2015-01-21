"""
elCID OPAL implementation
"""
from django.conf import settings

from opal.utils import OpalApplication

class Application(OpalApplication):
    schema_module = 'elcid.schema'
    flow_module   = 'elcid.flow'
