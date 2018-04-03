from search.search_rule import SearchRule, ModelSearchRule


def extract_schema_for_model(model):
    serialised = {
        'name': model.get_api_name(),
        'display_name': model.get_display_name(),
        'fields': model.build_field_schema(),
        'description': model.get_description()
    }

    if hasattr(model, 'get_icon'):
        serialised["icon"] = model.get_icon()
    for field in serialised["fields"]:
        field["type_display_name"] = model.get_human_readable_type(
            field["name"]
        )

    new_fields = []

    for field in serialised['fields']:
        field["type_display_name"] = model.get_human_readable_type(
            field["name"]
        )
        new_fields.append(field)
    serialised['fields'] = new_fields
    serialised["fields"] = sorted(
        serialised["fields"], key=lambda x: x["title"]
    )
    return serialised


def extract_search_schema():
    """
        Creates the search schema, ie a combination of all roles
        and subrecords (that are advanced_searchable)
    """
    return [i.to_search_dict() for i in SearchRule.list()]


def extract_download_schema_for_model(model):
    """
        similar to extract_search_schema but excludes fields
        that one cannot extract
    """
    return ModelSearchRule(model).to_extract_dict()
