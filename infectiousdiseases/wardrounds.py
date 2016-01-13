from wardround import WardRound
from opal.models import Episode

class ConsultantReview(WardRound):
    name = "Consultant review"
    description = "Patients diagnosis review"
    filter_template = "wardrounds/consultant_review_filter.html"
    detail_template = 'wardrounds/discharged_detail.html'
    filters = {
        'consultant_at_discharge': 'episode.consultant_at_discharge[0].consultant === value'
    }

    @staticmethod
    def episodes():
        episodes = Episode.objects.exclude(discharge_date=None)
        episodes = episodes.exclude(consultantatdischarge__consultant_fk=None)
        episodes = episodes.filter(primarydiagnosis__confirmed=False)
        return episodes.order_by("-discharge_date")
