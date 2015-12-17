from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404

from opal.core.views import _build_json_response
from opal import models as opal_models


class MicroHaemDataView(View):
    """
    Return a serialised view of the patient.
    """
    def get(self, *args, **kwargs):
        patient_id = kwargs.get("patient_id")
        patient = get_object_or_404(opal_models.Patient, id=patient_id)

        serialised = opal_models.Episode.objects.serialised(
            self.request.user,
            patient.episode_set.all()
        )

        return _build_json_response(serialised)


class MicroHaemTemplateView(TemplateView):
    template_name = 'patient_notes.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PatientNotesTemplateView, self).get_context_data(*args, **kwargs)
        context['models'] = {m.__name__: m for m in subrecords()}
        context['inline_forms'] = getattr(app, "patient_view_forms", [])
        return context
