from django.db.models import Q
from opal.core.search.queries import DatabaseQuery
from gloss_api import demographics_query


class GlossQuery(DatabaseQuery):
    def patients_as_json(self):
        exists_in_elcid = super(GlossQuery, self).get_patients()

        if exists_in_elcid:
            return [e.to_dict(self.user) for e in exists_in_elcid]
        else:
            if len(self.query) == 1:
                if self.query[0]["field"] == "Hospital Number":
                    return demographics_query(self.query[0]["query"])
        return []
