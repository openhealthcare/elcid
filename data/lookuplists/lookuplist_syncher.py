import csv
import json
import sys
import pprint

# a simple lookup list loader
# takes in a csv, with the headers name, synonym 1, synonym 2, synonym 3
# takes in the type of model e.g. micro_test_single_test_pos_neg_equiv
# takes in the lookuplists.json file
# syncs the 2

class Differ(object):
    def __init__(self, lookuplist_type, to_load_csv, lookuplist_file="lookuplists.json"):
        self.lookuplist_type = lookuplist_type
        self.to_load_csv = to_load_csv
        self.lookuplist_file = lookuplist_file

    def names_to_synonyms(self, some_json):
        names_to_synonyms = {}

        for row in some_json:
            name = row["name"].lower()
            names_to_synonyms[name] = set(i.lower() for i in row["synonyms"])

        return names_to_synonyms

    def synonym_columns(self, csv_dict):
        result = set()
        for k, v in csv_dict.iteritems():
            if "synonym" in k.lower() and v and len(v.strip()):
                result.add(v.strip())
        return result

    def new_list(self):
        names_to_synonyms = {}
        with open(self.to_load_csv, 'rb') as csvfile:
            rows = csv.DictReader(csvfile)

            for row in rows:
                synonymn_columns = self.synonym_columns(row)
                synonymn_columns = set(i.lower() for i in synonymn_columns)
                names_to_synonyms[row["Name"].lower()] = synonymn_columns

        return names_to_synonyms

    def old_list(self):
        with open(self.lookuplist_file, 'r') as data_file:
            existing_json = json.load(data_file).get(self.lookuplist_type, [])
            return self.names_to_synonyms(existing_json)

    def get_synonyms(self, names_to_synonyms_dict):
        result = set()

        for synonyms in names_to_synonyms_dict.itervalues():
            result = result.union(synonyms)
        return result

    def diff_lists(self):
        new_dict = self.new_list()
        old_dict = self.old_list()
        new_names = set(new_dict.keys())
        old_names = set(old_dict.keys())
        new_synonyms = self.get_synonyms(new_dict)
        old_synonyms = self.get_synonyms(old_dict)

        existing_names_as_new_synonyms = new_synonyms.intersection(old_names)

        new_names_as_old_synonyms = old_synonyms.intersection(new_names)

        print "existing names as new synonyms"
        pprint.pprint(existing_names_as_new_synonyms)

        print "new names as existing synonyms"
        pprint.pprint(new_names_as_old_synonyms)

        names_diff = new_names.difference(old_names)
        names_diff = names_diff.difference(new_names_as_old_synonyms)

        print "new names"
        pprint.pprint(names_diff)
        print "========"
        # all_new_synonyms = [i]
        # synonyms_diff = new_synonyms.diff(old_synonyms)
        print "synonyms diff"
        common_names = new_names.intersection(old_names)

        names_to_add = {i: v for i, v in new_dict.iteritems() if i in names_diff}
        synonyms_to_add = {}

        for common_name in common_names:
            old_row_synonyms = old_dict[common_name]
            new_row_synonyms = new_dict[common_name]
            synonyms_diff = new_row_synonyms.difference(old_row_synonyms)
            if synonyms_diff:
                print "new synonyms for {0}".format(common_name)
                pprint.pprint(synonyms_diff)
                print "========"
                synonyms_to_add[common_name] = synonyms_diff

        return names_to_add, synonyms_to_add

    def case_synonyms(self, synonyms):
        cased_synonyms = []

        for synonym in synonyms:
            if synonym.islower():
                cased_synonyms.append(synonym.title())
            else:
                cased_synonyms.append(synonym)

        return cased_synonyms

    def update_names_for_case_sensitivity(self, names_to_add):
        cased = {}
        result = []
        with open(self.to_load_csv, 'rb') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                name = row["Name"]
                if name.lower() in names_to_add:
                    if name.islower():
                        name = name.title()

                    synonyms = self.synonym_columns(row)
                    cased[name] = self.case_synonyms(synonyms)

        for name, synonyms in cased.iteritems():
            if not synonyms:
                synonyms = []
            result.append(dict(name=name, synonyms=sorted(synonyms)))

        return result

    def update_synonyms_for_case_sensitivity(self, synonyms_to_add, old_json):
        for d in old_json:
            if d["name"].lower() in synonyms_to_add:
                new_synonyms = synonyms_to_add[d["name"].lower()]
                new_synonyms = self.case_synonyms(new_synonyms)
                synonyms = new_synonyms + d["synonyms"]
                d["synonyms"] = sorted(synonyms)

        return old_json

    def sync(self):
        names_to_add, synonyms_to_add = self.diff_lists()

        with open(self.lookuplist_file, 'r') as data_file:
            all_existing_json = json.load(data_file)
            existing_json = all_existing_json.get(self.lookuplist_type, [])
            print "existing json length %s" % len(existing_json)
            new_json = self.update_synonyms_for_case_sensitivity(synonyms_to_add, existing_json)
            new_names = self.update_names_for_case_sensitivity(names_to_add)
            new_json = new_json + new_names
            print "new json length %s" % len(new_json)
            all_existing_json[self.lookuplist_type] = new_json

            to_write_file = self.lookuplist_file

            if not to_write_file.endswith(".new"):
                to_write_file = "{}.new".format(to_write_file)

            with open(to_write_file, 'w+') as data_file:
                json.dump(all_existing_json, data_file, sort_keys=True, indent=2, separators=(',', ': '))


def run(lookuplist_type, to_load_csv, lookuplist_file):
    differ = Differ(lookuplist_type, to_load_csv, lookuplist_file=lookuplist_file)
    differ.sync()

if __name__ == "__main__":
    run(*sys.argv[1:4])
