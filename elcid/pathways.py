from pathway import pathways

from elcid import models


class CDiffAddPatient(pathways.WizardPathway):
    display_name = 'Add C.Difficile Patient'
    slug = 'addcdiff'

    steps = [
        models.Demographics,
        pathways.Step(
            template_url='/templates/cdiff_ass.html',
            display_name='New Diagnosis Assessment',
            icon='fa fa-doctor'
        ),
        pathways.Step(
            display_name='Confirm',
            icon='fa fa-ok',
            template_url='/templates/cdiff_confirm.html'
        )
    ]
