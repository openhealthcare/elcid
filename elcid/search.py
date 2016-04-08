from opal.core.search.queries import DatabaseQuery
from django.conf import settings
import requests
import json


def query_gloss(hospital_number):
    base_url = settings.GLOSS_URL_BASE
    url = "{0}/api/demographics/{1}".format(base_url, hospital_number)
    result = json.loads(requests.get(url).content)

    if result["status"] == "success":
        demographics = result["messages"]["demographics"]
        for demographic in demographics:
            demographic["hospital_number"] = hospital_number
            demographic["sourced_from_upstream"] = True

        return [{"demographics": demographics}]
    else:
        # TODO: handle this better
        return []


class GlossQuery(DatabaseQuery):
    def patients_as_json(self):
        exists_in_elcid = super(GlossQuery, self).get_patients()

        if exists_in_elcid:
            return [e.to_dict(self.user) for e in exists_in_elcid]
        else:
            if len(self.query) == 1:
                if self.query[0]["field"] == "Hospital Number":
                    return query_gloss(self.query[0]["query"])

        return []
