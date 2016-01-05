from opal.core.patient_lists import TaggedPatientList
from elcid import models


class InfectionControl(TaggedPatientList):
    tag = "infectioncontrol"

    schema = [
        models.Demographics,
        models.Location,
        models.MicrobiologyTest,
    ]
