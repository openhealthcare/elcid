from opal.core.patient_lists import PatientList, TaggedPatientList
from elcid import models


class InfectionControl(TaggedPatientList, PatientList):
    tag = "infectioncontrol"

    schema = [
        models.Demographics,
        models.Location,
        models.MicrobiologyTest,
    ]
