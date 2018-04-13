from search.search_rule import SearchRule
from opal.models import Episode


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
    if model == Episode:
        api_name = "episode"
    else:
        api_name = model.get_api_name()

    return SearchRule.get(api_name).to_extract_dict()
