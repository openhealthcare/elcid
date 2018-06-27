"""
Opal Search views
"""
import datetime
import itertools
import json
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import View, TemplateView
from django.core.paginator import Paginator

from rest_framework import status

from opal import models
from django.contrib.auth.mixins import LoginRequiredMixin
from opal.core.views import (
    json_response, _get_request_data, with_no_caching
)
from search import queries
from search import search_rules
from search import extract_rules
from search import constants
from search.extract import (
    zip_archive, async_extract, get_datadictionary_context
)
from search import models as search_models

PAGINATION_AMOUNT = 10


class SearchIndexView(LoginRequiredMixin, TemplateView):
    """
    Main entrypoint into the pathway portal service.
    This is the entry point that loads in the pathway.
    """
    template_name = 'search/index.html'


class SaveFilterModalView(TemplateView):
    template_name = 'save_filter_modal.html'


class SearchTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'search/search.html'


class ExtractTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'search/extract.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(ExtractTemplateView, self).get_context_data(
            *args, **kwargs
        )
        ctx["widgets"] = search_rules.SearchRule.widgets(
            self.request.user
        )
        descriptions = search_rules.SearchRule.widget_descriptions(
            self.request.user
        )
        ctx["widget_descriptions"] = descriptions

        search_descriptions = []

        rules = search_rules.SearchRule.list_rules(
            self.request.user
        )

        for rule in rules:
            for field in rule.get_fields():
                search_descriptions.append(
                    (rule, field, field.get_description_template(),)
                )

        ctx["search_descriptions"] = search_descriptions

        extract_descriptions = []

        rules = extract_rules.ExtractRule.list_rules(
            self.request.user
        )

        for rule in rules:
            for field in rule.get_fields_for_schema():
                extract_descriptions.append(
                    (rule, field, field.get_description_template(),)
                )

        ctx["extract_descriptions"] = extract_descriptions
        ctx["description_templates"] = set(i[2] for i in itertools.chain(
            ctx["search_descriptions"], ctx["extract_descriptions"]
        ))

        pd = self.request.user.profile.roles.filter(
            name=constants.EXTRACT_PERSONAL_DETAILS
        ).exists()

        ctx["EXTRACT_PERSONAL_DETAILS"] = pd

        ctx.update(get_datadictionary_context(self.request.user, in_page=True))
        return ctx


def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper


def ajax_login_required_view(view):
    @wraps(view)
    def wrapper(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise PermissionDenied
        return view(self, *args, **kwargs)
    return wrapper


def _add_pagination(eps, page_number):
    paginator = Paginator(eps, PAGINATION_AMOUNT)
    results = {
        "object_list": paginator.page(page_number).object_list,
        "page_number": page_number,
        "total_pages": paginator.num_pages,
        "total_count": len(eps),
    }
    return results


@with_no_caching
@require_http_methods(['GET'])
@ajax_login_required
def patient_search_view(request):
    hospital_number = request.GET.get("hospital_number")

    if hospital_number is None:
        return json_response({'error': "No search terms"}, 400)

    criteria = [{
        "query_type": "Equals",
        "value": hospital_number,
        "field": "hospital_number",
        'combine': 'and',
        'rule': u'demographics',
    }]

    query = queries.create_query(request.user, criteria)
    return json_response(query.patients_as_json())


@with_no_caching
@require_http_methods(['GET'])
@ajax_login_required
def simple_search_view(request):
    page_number = int(request.GET.get("page_number", 1))
    query_string = request.GET.get("query")
    if not query_string:
        return json_response({'error': "No search terms"}, 400)

    query = queries.create_query(request.user, query_string)
    patients = query.fuzzy_query()
    paginated = _add_pagination(patients, page_number)
    paginated_patients = paginated["object_list"]

    # on postgres it blows up if we don't manually manage this
    if not paginated_patients:
        paginated_patients = models.Patient.objects.none()

    episodes = models.Episode.objects.filter(
        id__in=paginated_patients.values_list("episode__id", flat=True)
    )
    paginated["object_list"] = query.get_aggregate_patients_from_episodes(
        episodes
    )

    return json_response(paginated)


def get_paginated_reponse(query, patients, page_number):
    paginated = _add_pagination(patients, page_number)
    paginated_patients = paginated["object_list"]

    # on postgres it blows up if we don't manually manage this
    if not paginated_patients:
        paginated_patients = models.Patient.objects.none()

    episodes = models.Episode.objects.filter(
        id__in=paginated_patients.values_list("episode__id", flat=True)
    )
    paginated["object_list"] = query.get_aggregate_patients_from_episodes(
        episodes
    )
    return paginated


class ExtractSearchView(View):
    @ajax_login_required_view
    def post(self, *args, **kwargs):
        request_data = _get_request_data(self.request)
        page_number = 1

        from time import time
        import logging
        ts = time()

        if not request_data:
            return json_response(
                dict(error="No search criteria provied"),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if "page_number" in request_data[0]:
            page_number = request_data[0].pop("page_number", 1)

        query = queries.create_query(
            self.request.user,
            request_data,
        )
        if settings.OPTIMISED_SEARCH:
            patients = query.new_get_patients()
            response = get_paginated_reponse(query, patients, page_number)
        else:
            patient_summaries = query.get_patient_summaries()
            response = _add_pagination(patient_summaries, page_number)

        te = time()

        logging.info('search optiised %s: %2.4f sec' % (
            settings.OPTIMISED_SEARCH, te-ts
        ))

        return json_response(response)


class DownloadSearchView(View):
    @ajax_login_required_view
    def post(self, *args, **kwargs):
        if getattr(settings, 'EXTRACT_ASYNC', None):
            request_data = _get_request_data(self.request)
            criteria = request_data['criteria']
            data_slice = request_data.get('data_slice', None)
            extract_query = dict(
                criteria=json.loads(criteria),
            )
            if data_slice:
                extract_query["data_slice"] = json.loads(data_slice)
            search_models.ExtractQuery.objects.create(
                user=self.request.user,
                query_params=extract_query
            )
            extract_id = async_extract(
                self.request.user,
                extract_query
            )
            return json_response({'extract_id': extract_id})

        criteria = json.loads(self.request.POST['criteria'])
        if 'data_slice' in self.request.POST:
            data_slice = json.loads(self.request.POST['data_slice'])
        else:
            data_slice = None

        to_save = dict(
            criteria=criteria,
            data_slice=data_slice
        )

        search_models.ExtractQuery.objects.create(
            user=self.request.user,
            query_params=to_save
        )

        query = queries.create_query(
            self.request.user, criteria
        )
        episodes = query.get_episodes()
        fname = zip_archive(
            episodes,
            query.description(),
            self.request.user,
            fields=data_slice
        )
        resp = HttpResponse(open(fname, 'rb').read())
        disp = 'attachment; filename="{0}extract{1}.zip"'.format(
            settings.OPAL_BRAND_NAME, datetime.datetime.now().isoformat())
        resp['Content-Disposition'] = disp
        return resp


class ExtractStatusView(View):
    @ajax_login_required_view
    def get(self, *args, **kwargs):
        """
        Tell the client about the state of the extract
        """
        from celery.result import AsyncResult
        from opal.core import celery
        task_id = kwargs['task_id']
        result = AsyncResult(id=task_id, app=celery.app)

        return json_response({'state': result.state})


class ExtractFileView(View):

    @ajax_login_required_view
    def get(self, *args, **kwargs):
        from celery.result import AsyncResult
        from opal.core import celery
        task_id = kwargs['task_id']
        result = AsyncResult(id=task_id, app=celery.app)
        if result.state != 'SUCCESS':
            raise ValueError('Wrong Task Larry!')
        fname = result.get()
        with open(fname, 'rb') as fh:
            contents = fh.read()
        resp = HttpResponse(contents)
        disp = 'attachment; filename="{0}extract{1}.zip"'.format(
            settings.OPAL_BRAND_NAME, datetime.datetime.now().isoformat())
        resp['Content-Disposition'] = disp
        return resp
