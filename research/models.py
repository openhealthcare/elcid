"""
Models for the OPAL Research study plugin
"""
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from opal.models import EpisodeSubrecord, Synonym, Episode


class ResearchStudy(models.Model):
    """
    An individul research study being conducted.

    We store some metadata and study personnel by role.
    """
    name           = models.CharField(max_length=200)
    active         = models.BooleanField(default=False)
    clinical_lead  = models.ManyToManyField(User, blank=True, null=True,
                                            related_name='clinical_lead_user')
    researcher     = models.ManyToManyField(User, blank=True, null=True,
                                            related_name='researcher_user')
    research_nurse = models.ManyToManyField(User, blank=True, null=True,
                                            verbose_name='Research Practitioner',
                                            related_name='research_nurse_user')
    scientist      = models.ManyToManyField(User, blank=True, null=True,
                                            related_name='scientist_user')

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'Research Studies'

    @property
    def team_name(self):
        """
        Return the sanitised team name.
        """
        return self.name.lower().replace(' ', '_').replace('-', '_')


class StudyParticipation(EpisodeSubrecord):
    """
    Store details pertaining to an episode of care and how it relates to the
    current study.
    """
    _is_singleton = True
    _icon = 'fa fa-book'

    study_id = models.CharField(max_length=200, blank=True, null=True)


@receiver(models.signals.post_save, sender=ResearchStudy)
def create_teams_for_study(sender, **kwargs):
    """
    If we have just created a new study we should now set up the teams
    for that study.
    """
    if kwargs['created']:
        study = kwargs['instance']
        from opal.models import Team

        study_team = Team(name=study.team_name,
                          restricted=True,
                          direct_add=False,
                          title=study.name)
        study_team.save()

        teams = [
            ('Scientist', study.team_name + '_scientist'),
            ('Research Practitioner', study.team_name + '_research_practitioner')
        ]

        for title, name in teams:
            team = Team(name=name, title=title,
                        active=True, parent=study_team, restricted=True,
                        direct_add=False)
            team.save()
    return
