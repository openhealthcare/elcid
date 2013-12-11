"""
Dump a setting.
"""

import sys
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        print sys.argv[-1], '=', getattr(settings, sys.argv[-1])
