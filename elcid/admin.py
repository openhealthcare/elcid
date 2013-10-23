"""
Admin for elcid fields
"""
from django.contrib import admin
from opal.admin import SubRecordAdmin

from elcid import models

admin.site.register(models.Demographics, SubRecordAdmin)
admin.site.register(models.Location, SubRecordAdmin)
admin.site.register(models.Diagnosis, SubRecordAdmin)
admin.site.register(models.PastMedicalHistory, SubRecordAdmin)
admin.site.register(models.GeneralNote, SubRecordAdmin)
admin.site.register(models.Travel, SubRecordAdmin)
admin.site.register(models.Antimicrobial, SubRecordAdmin)
admin.site.register(models.MicrobiologyInput, SubRecordAdmin)
admin.site.register(models.Todo, SubRecordAdmin)
admin.site.register(models.MicrobiologyTest, SubRecordAdmin)
