"""
Admin for elcid fields
"""
from django.contrib import admin
from opal.admin import PatientSubRecordAdmin, EpisodeSubRecordAdmin

from elcid import models

from reversion import models as rmodels


class NotMergedFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'review status'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('not_merged', 'not merged'),
            ('not_reviewed', 'not reviewed'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'not_merged':
            return queryset.exclude(merged=True)
        if self.value() == 'not_reviewed':
            return queryset.exclude(reviewed=True)


class DuplicatePatientAdmin(admin.ModelAdmin):
    list_filter = (NotMergedFilter,)

admin.site.register(models.DuplicatePatient, DuplicatePatientAdmin)
admin.site.register(rmodels.Version, admin.ModelAdmin)
admin.site.register(rmodels.Revision, admin.ModelAdmin)
