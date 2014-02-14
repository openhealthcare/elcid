"""
Admin for elcid fields
"""
from django.contrib import admin
from opal.admin import PatientSubRecordAdmin, EpisodeSubRecordAdmin

from elcid import models

# for subclass in models.PatientSubrecord.__subclasses__():
#     admin.site.register(subclass, PatientSubRecordAdmin)

# for subclass in models.EpisodeSubrecord.__subclasses__():
#     admin.site.register(subclass, EpisodeSubRecordAdmin)

from reversion import models as rmodels

admin.site.register(rmodels.Version, admin.ModelAdmin)
admin.site.register(rmodels.Revision, admin.ModelAdmin)
