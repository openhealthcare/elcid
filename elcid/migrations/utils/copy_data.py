def update_content_types(apps, from_app, from_model, to_app, to_model):
    to_model = to_model.lower()
    ContentType = apps.get_model("contenttypes", "ContentType")

    # we delete the existing content types as
    # we assume they've been created by the previous Migration
    existing = ContentType.objects.filter(
        app_label__iexact=to_app, model__iexact=to_model
    )

    for i in existing:
        i.delete()

    cts = ContentType.objects.filter(
        app_label__iexact=from_app, model__iexact=from_model
    )

    cts.update(app_label=to_app, model=to_model.lower())
