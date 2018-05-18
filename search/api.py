from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from opal.core.views import json_response
from search.extract_rules import ExtractRule
from search.search_rules import SearchRule
from search import models


class ExtractQuerySchemaViewSet(viewsets.ViewSet):
    """
    Returns the schema to build our extract query builder
    """
    base_name = 'extract-query-schema'
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        return json_response(
            SearchRule.get_schemas(request.user)
        )


class ExtractSliceSchemaViewSet(viewsets.ViewSet):
    """
    Returns data dictionary for the extract slice
    """
    base_name = 'extract-slice-schema'
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        return json_response(
            ExtractRule.get_schemas(request.user)
        )


class ExtractQueryViewSet(viewsets.ViewSet):
    base_name = 'extract-query'
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        """
        Serialise a single user via UserProfile
        """
        extract_filter = models.ExtractQuery.objects.get(id=pk)
        return json_response(extract_filter.to_dict(request.user))
