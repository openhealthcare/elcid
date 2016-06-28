"""
Admin interfaces for our Research Study plugin
"""
from django.contrib import admin

from reversion.admin import VersionAdmin

from research import models

class StudyAdmin(VersionAdmin):
    list_display = ['name', 'active']
    list_filter = ['clinical_lead']
    filter_horizontal = ['clinical_lead', 'researcher', 'research_nurse', 'scientist']

admin.site.register(models.ResearchStudy, StudyAdmin)
