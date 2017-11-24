"""
A management command that takes in a string and sends it as an error.
"""
import logging
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('error', type=str)

    def handle(self, error, *args, **options):
        logger = logging.getLogger('error_emailer')
        logger.error(error)
