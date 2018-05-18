def migrate_forwards(apps, *args):
    PresentingComplaint = apps.get_model("elcid", "PresentingComplaint")
    Symptoms = apps.get_model("walkin", "Symptom")

    for symptoms_class in [PresentingComplaint, Symptoms]:
        for symptoms_instance in symptoms_class.objects.all():
            if symptoms_instance.symptom_fk:
                symptoms_instance.symptoms.add(
                    symptoms_instance.symptom_fk
                )
