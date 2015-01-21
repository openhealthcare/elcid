"""
elCID OPAL implementation
"""
from django.conf import settings

from opal.utils import OpalApplication

from elcid import flow, schema

class Application(OpalApplication):
    schema_module = schema
    flow_module   = flow
