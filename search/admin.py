from django.contrib import admin

from search.models import ExtractQuery

admin.site.register(ExtractQuery, admin.ModelAdmin)
