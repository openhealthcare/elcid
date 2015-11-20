from elcid.models import Diagnosis, Line, Antimicrobial, BloodCulture
from pathway.pathways import Pathway

class BloodCulturePathway(Pathway):
    title = "Blood Culture"
    steps = (
        Diagnosis,
        Line,
        Antimicrobial,
        BloodCulture,
    )

    def get_steps_info(self):
        steps_info = super(BloodCulturePathway, self).get_steps_info()
        steps_info["steps"].insert(0, (dict(
            template_url="/pathway/templates/find_patient_form.html",
            controller_class="FindPatientCtrl",
            title="find patient",
            icon="fa fa-user"
        )))

        # ths should be included in the step api
        line_title = getattr(Line, "_title", Line.get_display_name())
        line_step = next(i for i in steps_info["steps"] if i["title"] == line_title)
        line_step["template_url"] = "/pathway/templates/optional_line.html"
        line_step["controller_class"] = "LineController"
        return steps_info
