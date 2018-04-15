How to search an how to extract

Searchin uses Search Rules

A search rule is a discoverable feature.

By default all subrecords are wrapped in search rules.

To override a subrecord's search rule, create a search rule with the slug of a subrecords api name.

By default a search rule will allow you to search on all fields.

If you declare additional fields. These will be added.

If you declare a list of field names, then only
these will be searchable.

```
class EpisodeTeamSearchFieldRule(SearchFieldRule):
    def query(self, given_query):
        pass

class EpisodeTeamExtractFieldRule(ExtractFieldRule):
    def extract(self, instance):
        pass


class EpisodeSearchRule(SearchRule):
    display_name = "Episode"
    slug = "episode"
    model = Episode
    search_fields = (
      EpisodeTeamSearchFieldRule, "start", "end",
    )
    extract_fields = (
      EpisodeTeamExtractFieldRule, "start", "end", "patient_id"
    )

class Search



```
