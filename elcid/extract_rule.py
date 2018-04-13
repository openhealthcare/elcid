from search import subrecord_discoverable
from opal.core.discoverable import DiscoverableFeature


class ExtractRule(
    subrecord_discoverable.SubrecordDiscoverableMixin,
    DiscoverableFeature
):
    module_name = "extract_rule"
    fields = None
    display_name = ""
    slug = ""

    def get_model_fields(self):
        return self.model._get_fieldnames_to_extract()

    def to_extract_dict(self):
        fields = [i.to_dict() for i in self.get_fields()]
        fields = sorted(
            fields, key=lambda x: x["title"]
        )
        return dict(
            name=self.get_api_name(),
            display_name=self.get_display_name(),
            fields=fields,
            description=self.get_description()
        )
