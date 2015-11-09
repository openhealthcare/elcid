import csv
import json
import sys

# a simple lookup list loader
# takes in a csv, with the headers name, synonym 1, synonym 2, synonym 3
# takes in the type of model e.g. micro_test_single_test_pos_neg_equiv
# takes in the lookuplists.json file
# syncs the 2


class Loader(object):

    def __init__(self, lookuplist_type, to_load_csv, lookuplist_file="lookuplists.json"):
        self.lookuplist_type = lookuplist_type
        self.to_load_csv = to_load_csv
        self.lookuplist_file = lookuplist_file

    # we assume words that are abbreviated are already uppercase
    def case_it(self, word):
        if word.isupper():
            return word
        else:
            return word.title()

    def existing_terms_and_synonyms(self, existing_json):
        all_synonyms = set()
        names_to_synonyms = {}

        for row in existing_json:
            name = self.case_it(row["name"])
            names_to_synonyms[name] = set(row["synonyms"])
            all_synonyms = all_synonyms.union(self.case_it(i) for i in row["synonyms"])

        return names_to_synonyms, all_synonyms

    def synonym_columns(self, csv_dict):
        result = set()
        for k, v in csv_dict.iteritems():
            if "symptom" in k.lower():
                result.add(self.case_it(v))
        return result

    def new_list(self, existing_json):
        with open(self.to_load_csv, 'rb') as csvfile:
            rows = csv.DictReader(csvfile)
            names_to_synonyms, all_synonyms = self.existing_terms_and_synonyms(existing_json)

            for row in rows:
                name = self.case_it(row["Name"])
                if name in all_synonyms:
                    print "we already have {} as a synonym, skipping".format(name)
                else:
                    new_synonyms = self.synonym_columns(row)
                    if name in names_to_synonyms:
                        names_to_synonyms[name] = names_to_synonyms[name].union(new_synonyms)
                    else:
                        print "adding {}".format(name)
                        names_to_synonyms[name] = new_synonyms

        new_list = []
        alphabetical = sorted(names_to_synonyms.iterkeys())

        for name in alphabetical:
            new_dict = dict(name=self.case_it(name))
            synonyms = names_to_synonyms[name]
            new_dict["synonyms"] = sorted(self.case_it(i) for i in synonyms)
            new_list.append(new_dict)

        return new_list

    def update_list(self):
        with open(self.lookuplist_file, 'r') as data_file:
            existing_json = json.load(data_file)
            existing_json[self.lookuplist_type] = self.new_list(existing_json[self.lookuplist_type])
        with open(self.lookuplist_file, 'w') as data_file:
            json.dump(existing_json, data_file, sort_keys=True, indent=2, separators=(',', ': '))

    def sync(self):
        self.update_list()


def run(lookuplist_type, to_load_csv):
    loader = Loader(lookuplist_type, to_load_csv)
    loader.sync()

if __name__ == "__main__":
    run(*sys.argv[:2])
