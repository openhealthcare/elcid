from opal.core.search.queries import DatabaseQuery
from gloss_api import demographics_query


class GlossQuery(DatabaseQuery):

    def recursively_get_duplicate_patients(self, result):
        """ a patient could be merged with another patient add infinitum
        """

        # TODO make this handle if someones merged hospital_numbers into
        # themselves (shouldn't happen but you can't trust an external system)
        while result and "duplicate_patient" in result[0] and result[0]["duplicate_patient"] and result[0]["duplicate_patient"][0]["new_id"]:
            hospital_number = result[0]["duplicate_patient"][0]["new_id"]
            self.query[0]["query"] = hospital_number
            result = self.demographics_query()

        return result

    def demographics_query(self):
        exists_in_elcid = super(GlossQuery, self).get_patients()

        if exists_in_elcid:
            return [e.to_dict(self.user) for e in exists_in_elcid]
        else:
            if len(self.query) == 1:
                if self.query[0]["field"] == "Hospital Number":
                    return demographics_query(self.query[0]["query"])

        return []

    def patients_as_json(self):
        result = self.demographics_query()

        if result:
            duplicate_patient = result[0].get("duplicate_patient", [])

            if duplicate_patient:
                result[0]["merged"] = self.recursively_get_duplicate_patients(
                    result
                )
                result[0]["duplicate_patient"] = [
                    dict(
                        new_id=result[0]["merged"][0]["demographics"][0]["hospital_number"]
                    )
                ]

        return result
