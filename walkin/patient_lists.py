"""
Patient Lists for the Walkin service
"""
from obs import models as obsmodels
from opal.core import patient_lists

from elcid import models

from walkin import models as wimodels

# defined separately in order to be able to override title of column to Symptoms
presenting_complaint_column = patient_lists.Column(
    name=models.PresentingComplaint.get_api_name(),
    title="Symptoms8",
    singleton=models.PresentingComplaint._is_singleton,
    icon=getattr(models.PresentingComplaint, '_icon', ''),
    limit=getattr(models.PresentingComplaint, '_list_limit', None),
    template_path="records/walkin/presenting_complaint.html",
    detail_template_path="records/walkin/presenting_complaint.html",
)

class WalkinDoctor(patient_lists.TaggedPatientList):
    display_name = 'Walkin Doctor'
    direct_add = False
    tag = "walkin"
    subtag = "walkin_doctor"
    order = 12
    allow_edit_teams = False
    schema = [
        models.Demographics,
        models.Location,
        models.Travel,
        presenting_complaint_column,
        wimodels.ClinicalFindings,
        models.MicrobiologyTest,
        models.Diagnosis,
        obsmodels.Observation,
        models.Antimicrobial,
        models.MicrobiologyInput
    ]


class WalkinNurseTriage(patient_lists.TaggedPatientList):
    display_name = 'Walkin Nurse Triage'
    direct_add = False
    tag = "walkin"
    subtag = "walkin_triage"
    order = 11
    allow_edit_teams = False
    schema = [
        models.Demographics,
        models.Location,
        models.Allergies,
        models.Travel,
        presenting_complaint_column,
        models.MicrobiologyTest,
        obsmodels.Observation,
    ]


class WalkinReview(patient_lists.TaggedPatientList):
    display_name = 'Walkin Review'
    direct_add = False
    tag = "walkin"
    subtag = "walkin_review"
    order = 13
    allow_edit_teams = False
    schema = [
        models.Demographics,
        models.Location,
        models.Travel,
        presenting_complaint_column,
        wimodels.ClinicalFindings,
        models.MicrobiologyTest,
        models.Diagnosis,
        models.Antimicrobial,
        models.MicrobiologyInput,
        wimodels.Management
    ]

class WalkinListGroup(patient_lists.TabbedPatientListGroup):
    member_lists = [
        WalkinNurseTriage,
        WalkinDoctor,
        WalkinReview
    ]
