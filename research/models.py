"""
Models for the OPAL Research study plugin
"""
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from opal.core import lookuplists
from opal.models import EpisodeSubrecord
from opal.core.fields import ForeignKeyOrFreeText

"""
Fields for UCLH - specific Research studies.
"""

""" RiD RTI (http://www.rid-rti.eu/ ) """


class ResearchStudy(models.Model):
    """
    An individul research study being conducted.

    We store some metadata and study personnel by role.
    """
    name           = models.CharField(max_length=200)
    active         = models.BooleanField(default=False)
    clinical_lead  = models.ManyToManyField(User, related_name='clinical_lead_user')
    researcher     = models.ManyToManyField(User, related_name='researcher_user')
    research_nurse = models.ManyToManyField(User, verbose_name='Research Practitioner', related_name='research_nurse_user')
    scientist      = models.ManyToManyField(User, related_name='scientist_user')

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
    _advanced_searchable = False


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


class Specimin(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Specimen"


class LabtestDetails(lookuplists.LookupList):
    _advanced_searchable = False


class Organism_details(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name_plural = "Organism details"


class Checkpoints_assay(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Checkpoints assay values"
        verbose_name_plural = "Checkpoints assay values"


class Antimicrobial_susceptability(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Antimicrobial susceptability"
        verbose_name_plural = "Antimicrobial susceptibilities"


class Specimin_appearance(lookuplists.LookupList):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Specimen appearance"


class LabSpecimin(EpisodeSubrecord):
    _advanced_searchable = False

    class Meta:
        verbose_name = "Lab specimen appearance"

    _title = 'Lab Specimen'
    _sort = 'date_collected'
    _icon = 'fa fa-flask'

    specimin_type     = ForeignKeyOrFreeText(Specimin)
    date_collected    = models.DateField(blank=True, null=True)
    volume            = models.CharField(max_length=200, blank=True, null=True)
    appearance        = ForeignKeyOrFreeText(Specimin_appearance)
    epithelial_cell   = models.CharField(max_length=200, blank=True, null=True)
    white_blood_cells = models.CharField(max_length=200, blank=True, null=True)
    date_tested       = models.DateField(blank=True, null=True)
    external_id       = models.CharField(max_length=200, blank=True, null=True)
    biobanking        = models.NullBooleanField(default=False)
    biobanking_box    = models.CharField(max_length=200, blank=True, null=True)
    date_biobanked    = models.DateField(blank=True, null=True)
    volume_biobanked  = models.CharField(max_length=200, blank=True, null=True)


# This is based on the investigations record type from elCID
class LabTest(EpisodeSubrecord):
    _sort = 'date_ordered'
    _icon = 'fa fa-crosshairs'
    _advanced_searchable = False

    test                         = models.CharField(max_length=255)
    date_ordered                 = models.DateField(null=True, blank=True)
    details                      = models.CharField(max_length=255, blank=True)
    result                       = models.CharField(max_length=255, blank=True)
    significant_organism         = models.NullBooleanField(default=False)
    organism_details             = ForeignKeyOrFreeText(Organism_details)
    antimicrobials_susceptible   = ForeignKeyOrFreeText(Antimicrobial_susceptability,
                                                        related_name='susceptible')
    antimicrobials_intermediate  = ForeignKeyOrFreeText(Antimicrobial_susceptability,
                                                        related_name='intermediate')
    antimicrobials_resistant     = ForeignKeyOrFreeText(Antimicrobial_susceptability,
                                                        related_name='resistant')
    retrieved                    = models.NullBooleanField(default=False)
    date_retrieved               = models.DateField(null=True, blank=True)
    sweep_biobanked              = models.NullBooleanField(default=False)
    organism_biobanked           = models.NullBooleanField(default=False)
    freezer_box_number           = models.CharField(max_length=200, blank=True, null=True)
    esbl                         = models.NullBooleanField(default=False)
    carbapenemase                = models.NullBooleanField(default=False)


class RidRTIStudyDiagnosis(EpisodeSubrecord):
    """
    The RidRTI study Diagnosis.
    """
    _advanced_searchable = False
    diagnosis = models.CharField(max_length=255)


class RidRTITest(EpisodeSubrecord):
    """
    Results of the actual RiD RTI test !
    """
    _advanced_searchable = False

    test            = models.CharField(max_length=200, blank=True, null=True)
    notes           = models.TextField(blank=True, null=True)
    # HAP/VAP results
    pseudomonas_aeruginosa = models.NullBooleanField(default=False)
    acinetobacter_baumannii = models.NullBooleanField(default=False)
    senotophomonas_maltophilia = models.NullBooleanField(default=False)
    klebsiella_spp = models.NullBooleanField(default=False)
    enterobacter_spp = models.NullBooleanField(default=False)
    staphylococcus_aureus = models.NullBooleanField(default=False)
    staphylococcus_mrsa = models.NullBooleanField(default=False)
    ctx_m = models.NullBooleanField(default=False)
    shv_esbl = models.NullBooleanField(default=False)
    tem_esbl = models.NullBooleanField(default=False)
    vim = models.NullBooleanField(default=False)
    imp = models.NullBooleanField(default=False)
    ndm = models.NullBooleanField(default=False)
    kpc = models.NullBooleanField(default=False)
    oxa_48 = models.NullBooleanField(default=False)
    meca = models.NullBooleanField(default=False)
    # CAP results
    mycoplasma_pneumoniae = models.NullBooleanField(default=False)
    chlamydophila_pneumoniae = models.NullBooleanField(default=False)
    legionella_pneumophila = models.NullBooleanField(default=False)
    # (Mycobacterium tuberculosis complex) = models.NullBooleanField(default=False)
    mtc = models.NullBooleanField(default=False)
    haemophilus_influenzae = models.NullBooleanField(default=False)
    streptococcus_pneumoniae = models.NullBooleanField(default=False)
    rsva = models.NullBooleanField(default=False)
    rsvb = models.NullBooleanField(default=False)
    influenza_a = models.NullBooleanField(default=False)
    influenza_b      = models.NullBooleanField(default=False)
    cap_coronavirus_oc43 = models.NullBooleanField(default=False)
    cap_coronavirus_hku1 = models.NullBooleanField(default=False)
    cap_coronavirus_nl63 = models.NullBooleanField(default=False)
    cap_coronavirus_229e = models.NullBooleanField(default=False)
    # ORTI results
    nocardia_spp = models.NullBooleanField(default=False)
    rhodococcus_equi = models.NullBooleanField(default=False)
    # (Aspergillus spp Cryptococcus neoformans)
    aspergillus_spp = models.NullBooleanField(default=False)
    cryptococcus_neoformans = models.NullBooleanField(default=False)
    pneumocystis_jiroveci = models.NullBooleanField(default=False)
    orti_coronavirus_oc43 = models.NullBooleanField(default=False)
    orti_coronavirus_hku1 = models.NullBooleanField(default=False)
    orti_coronavirus_nl63 = models.NullBooleanField(default=False)
    orti_coronavirus_229e = models.NullBooleanField(default=False)

    class Meta:
        verbose_name = "RiD-RTI"


class CheckpointsAssay(EpisodeSubrecord):
    _is_singleton = True
    _advanced_searchable = False

    acc = models.NullBooleanField(default=False)
    act_mir = models.NullBooleanField(default=False)
    bel = models.NullBooleanField(default=False)
    cmy_i_mox = models.NullBooleanField(default=False)
    cmy_ii = models.NullBooleanField(default=False)
    ctx_m_1_group = models.NullBooleanField(default=False)
    ctx_m_1_like = models.NullBooleanField(default=False)
    ctx_m_15_like = models.NullBooleanField(default=False)
    ctx_m_2_group = models.NullBooleanField(default=False)
    ctx_m_3_like = models.NullBooleanField(default=False)
    ctx_m_32_like = models.NullBooleanField(default=False)
    ctx_m_8_25_group = models.NullBooleanField(default=False)
    ctx_m_9_group = models.NullBooleanField(default=False)
    dha = models.NullBooleanField(default=False)
    fox = models.NullBooleanField(default=False)
    ges = models.NullBooleanField(default=False)
    gim = models.NullBooleanField(default=False)
    imp = models.NullBooleanField(default=False)
    kpc = models.NullBooleanField(default=False)
    ndm = models.NullBooleanField(default=False)
    oxa_23_like = models.NullBooleanField(default=False)
    oxa_24_like = models.NullBooleanField(default=False)
    oxa_48_like = models.NullBooleanField(default=False)
    oxa_58_like = models.NullBooleanField(default=False)
    per = models.NullBooleanField(default=False)
    shv_e240k = models.NullBooleanField(default=False)
    shv_g238a = models.NullBooleanField(default=False)
    shv_g238s = models.NullBooleanField(default=False)
    shv_wt = models.NullBooleanField(default=False)
    spm = models.NullBooleanField(default=False)
    tem_e104k = models.NullBooleanField(default=False)
    tem_g238s = models.NullBooleanField(default=False)
    tem_r164c = models.NullBooleanField(default=False)
    tem_r164h = models.NullBooleanField(default=False)
    tem_r164s = models.NullBooleanField(default=False)
    tem_wt = models.NullBooleanField(default=False)
    veb = models.NullBooleanField(default=False)
    vim = models.NullBooleanField(default=False)

    negative = models.NullBooleanField(default=False)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Checkpoints assay"
