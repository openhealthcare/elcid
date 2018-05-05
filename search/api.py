from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from opal.core.views import json_response
from search.extract_rules import ExtractRule
from search.search_rules import SearchRule


class ExtractQuerySchemaViewSet(viewsets.ViewSet):
    """
    Returns the schema to build our extract query builder
    """
    base_name = 'extract-schema'
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        return json_response(
            SearchRule.get_schemas(request.user)
        )


class ExtractSliceSchemaViewSet(viewsets.ViewSet):
    """
    Returns data dictionary for the extract slice
    """
    base_name = 'data-dictionary'
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        return json_response(
            ExtractRule.get_schemas(request.user)
        )
