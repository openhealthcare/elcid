"""
Research views!
"""
from django.views.generic import TemplateView

class ResearchTemplateView(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.name = kwargs['name']
        return super(ResearchTemplateView, self).dispatch(*args, **kwargs)

    def get_template_names(self, *args, **kwargs):
        return ['research/'+self.name]

