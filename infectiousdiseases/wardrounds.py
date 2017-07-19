"""
Wardrounds for ID
"""
from wardround.wardrounds import WardRound
from opal.models import Episode
from elcid.models import Consultant


class ConsultantReview(WardRound):
    display_name = "Consultant review"
    description = "Patients diagnosis review"
    filter_template = "wardrounds/consultant_review_filter.html"
    detail_template = 'wardrounds/discharged_detail.html'

    def episodes(self):
        consultant_name = self.request.GET.get("consultant_at_discharge", None)

        episodes = Episode.objects.exclude(end=None)
        episodes = episodes.exclude(consultantatdischarge__consultant_fk=None)
        episodes = episodes.filter(primarydiagnosis__confirmed=False)

        if consultant_name:
            consultant = Consultant.objects.get(name=consultant_name)
            episodes = episodes.filter(
                consultantatdischarge__consultant_fk=consultant.id
            )

        return episodes.order_by("-end")
