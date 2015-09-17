"""
[Virtual] Ward Round implementations
"""
import datetime

from django.db.models import Q

from opal.models import Episode, Tagging
from wardround import WardRound
from obs import models as obsmodels

from elcid import models

class HistoricTagsMixin(object):
    
    @classmethod
    def to_dict(klass, user):
        """
        We're overriding this so that we can set the extra flag on historic Tags.
        """
        return dict(name=klass.name, 
                    description=klass.description,
                    episodes=Episode.objects.serialised(user, klass.episodes(),
                                                        episode_history=True,
                                                        historic_tags=True),
                    filters=klass.filters)


class Discharged(HistoricTagsMixin, WardRound):
    name = 'Discharged last week'
    description = 'Patients discharged in the last week'

    filter_template = 'wardrounds/discharged_filter.html'
    detail_template = 'wardrounds/discharged_detail.html'
    filters = {
        'team': 'episode.tagging[0][value]'
    }
    
    @staticmethod
    def episodes():
        today = datetime.date.today()
        two_weeks_ago = today - datetime.timedelta(days=7)
        episodes = Episode.objects.filter(
            category__in=['inpatient', 'Walkin'],
            discharge_date__gte=two_weeks_ago)
        return episodes

    
class MicroHaem(WardRound):
    name        = 'Micro Haem'
    description = 'All patients on the Micro haem list in ward location order'

    @staticmethod
    def episodes():
        return Episode.objects.filter(active=True, tagging__team__name='micro_haem')


# class FinalDiagnosisReview(HistoricTagsMixin, WardRound):
#     name        = 'Final Diagnosis Review'
#     description = 'Discharged Patients with a final diagnosis for consultant review.'
    
#     filter_template = 'wardrounds/final_diagnosis_filter.html'
#     filters    = {
#         'discharge_from': 'episode.discharge_date >= moment(value, "DD-MM-YYYY")',
#         'discharge_to'  : 'episode.discharge_date <= moment(value, "DD-MM-YYYY")',
#         'team'          : 'episode.tagging[0][value]'
#     }
    
#     @staticmethod
#     def episodes():
#         unconfirmed = models.PrimaryDiagnosis.objects.filter(confirmed=False).filter(Q())

#         def interesting(episode):
#             """
#             Is episode interesting for the FDR?
#             """
#             if not episode.is_discharged:
#                 return False
#             interesting_teams = set(['id_inpatients', 
#                                      'tropical_diseases',
#                                      'immune_inpatients'])
#             return bool(interesting_teams.intersection(episode.get_tag_names(None, historic=True)))
            
#         return set([d.episode for d in unconfirmed if interesting(d.episode)])

#     @staticmethod
#     def schema():
#         return [
#             models.Demographics,
#             models.Location,
#             models.Diagnosis,
#             models.MicrobiologyTest,
#             models.Antimicrobial,
#             models.PrimaryDiagnosis,
#             models.SecondaryDiagnosis
#         ]


class OPATReviewList(WardRound):
    name = 'OPAT Review'
    description = 'Final review of OPAT patients post end-of-treatment'

    @staticmethod
    def episodes():
        review_ready = models.OPATMeta.objects.filter(review_date__lte=datetime.date.today())
        return set([om.episode for om in review_ready
                    if om.episode.opatoutcome_set.get().treatment_outcome is None])

    detail_template = 'wardrounds/opat_detail.html'


class OPATCurrentList(WardRound):
    name        = 'OPAT Current'
    description = 'All patients on the OPAT current list'

    @staticmethod
    def episodes():
        return Episode.objects.filter(active=True, tagging__team__name='opat_current')
