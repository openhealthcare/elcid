import json
from django.utils.functional import cached_property

TRANSLATION_FILE = "./data/nors_translations.json"


class Translator(object):
    @cached_property
    def json_file(self):
        with open(TRANSLATION_FILE) as tf:
            result = json.load(tf)
        return result

    @property
    def antimicrobials(self):
        return result["antimicrobials"]

    @property
    def infective_diagnosis(self):
        return result["antinfective_diagnosis"]
