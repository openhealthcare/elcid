import csv
import os
import dateutil.parser
from collections import defaultdict, Counter


def get_file_path(file_name):
    return os.path.join("/Users/fredkingham/Downloads/opat_extract", file_name)


def get_row_from_episode_id(episode_id, rows):
    try:
        return next(row for row in rows if row["episode_id"] == episode_id)
    except StopIteration:
        return


def get_reporting_period(pid_row):
    time_field = None
    for field in ["created", "updated"]:
        if not time_field and len(pid_row[field].strip()) and not pid_row[field] == "None":
            time_field = dateutil.parser.parse(pid_row[field])

    if not time_field:
        # not sure how to handle these skip them for the mo
        pid_row["reportingperiod"] = "None_NA"
    else:
        year = time_field.year
        quarter = ((time_field.month -1) / 3) + 1
        pid_row["reportingperiod"] = "{0}_{1}".format(year, quarter)


def get_opat_acceptance_for_episode(episode_id):
    with open(get_file_path("location.csv"), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["episode_id"] == episode_id:
                result = row
                break
    if not result["opat_acceptance"] or result["opat_acceptance"] == "None":
        result["opat_acceptance"] = None
    else:
        result["opat_acceptance"] = dateutil.parser.parse(result["opat_acceptance"]).date()

    if not result["opat_referral"] or result["opat_referral"] == "None":
        result["opat_referral"] = None
    else:
        result["opat_referral"] = dateutil.parser.parse(result["opat_referral"]).date()
    return result


def generate_reporting_periods(csv_rows):
    result = []
    # generate reporting period
    for row in csv_rows:
        get_reporting_period(row)
        result.append(row)
    return result


def drugs_union(pid_rows):
    # get episodes ids that had iv and werenot delivered by the inpatient team
    # we then do a union with opat eacceptences
    result = []
    episodes_with_ivs = {}
    with open(get_file_path("antimicrobial.csv"), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        ignore = set(["Inpatient Team", ""])
        rows = [row for row in reader if row["delivered_by"] not in ignore]
        for anitmicrobial_row in rows:
            if row["route"] == "IV":
                episodes_with_ivs.add(row["episode_id"])

        for row in rows:
            if row["start_date"] and row["end_date"]:
                if not row["end_date"] == "None":
                    if not row["start_date"] == "None":
                        row["start_date"] = dateutil.parser.parse(row["start_date"]).date()
                        row["end_date"] = dateutil.parser.parse(row["end_date"]).date()
                        row["duration"] = (row["end_date"] - row["start_date"]).days + 1

            if "duration" not in row:
                continue

            row["had_iv"] = row["episode_id"] in episodes_with_ivs
            pid_row = get_row_from_episode_id(row["episode_id"], pid_rows)
            opat_acceptance = get_opat_acceptance_for_episode(row["episode_id"])

            if not opat_acceptance["opat_acceptance"]:
                continue

            before_opat = (opat_acceptance["opat_acceptance"] - row["start_date"]).days
            row["opat_acceptance"] = opat_acceptance["opat_acceptance"]

            if before_opat > 0:
                row["duration"] = row["duration"] - before_opat

            if not row["duration"] > 0:
                continue

            if not row["episode_id"] in episodes_with_ivs:
                continue

            # if they don't have a pid row skip it for the time being
            if pid_row:
                row.update(pid_row)
                result.append(row)

    return result


def generate_anti_infectives():
    rows = generate_pid()

    rows = drugs_union(rows)
    defaultdict(list)
    sliced_data = defaultdict(list)

    def get_key(row):
        return (
            # row["duration"],
            row["drug"],
            row["infective_diagnosis"],
            row["reportingperiod"],
        )

    for row in rows:
        key = get_key(row)
        sliced_data[key].append(row)

    result = []

    for data_slice_key, value in sliced_data.items():
        counter = max(Counter(i["episode_id"] for i in value).values())
        result.append({
            "drug": data_slice_key[0],
            "infective_diagnosis": data_slice_key[1],
            "reportingperiod": data_slice_key[2],
            "duration.max": str(max(v["duration"] for v in value)),
            "count.max": str(counter)
        })

    reporting_periods = list(set(i["reportingperiod"] for i in result))

    result.sort(key=lambda x: x["infective_diagnosis"])
    result.sort(key=lambda x: x["drug"])

    for reporting_period in reporting_periods:
        cut = [i for i in result if i["reportingperiod"] == reporting_period]
        compare_with_file(
            cut,
            "/Users/fredkingham/Downloads/opat_extract/Anti-infectives by PID and Episodes_ {} .csv".format(reporting_period)
        )


def compare_with_file(result, file_name):
    with open(get_file_path(file_name), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        for row_num, row in enumerate(reader):
            if not row == result[row_num]:
                import ipdb; ipdb.set_trace()
                return


def filter_unknown_categorised_infective_diagnosis(rows):
    for row in rows:
        if row["infective_diagnosis_ft"] and len(row["infective_diagnosis_ft"]):
            row["infective_diagnosis"] = "Other - Free Text"
    return rows


def remove_those_who_have_not_completed(rows):
    return [row for row in rows if row["outcome_stage"] == "Completed Therapy"]


def remove_duplicates(rows):
    result = {}
    for row in rows:
        key = (row["episode_id"], row["outcome_stage"],)
        if key not in result:
            result[key] = row

    return result.values()


def remove_rejected(rows):
    episode_ids = set()
    with open(get_file_path("opat_rejection.csv"), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        episode_ids = {i["episode_id"] for i in reader}
    return [i for i in rows if i["episode_id"] not in episode_ids]


def generate_pid():
    rows = []
    with open(get_file_path("opat_outcome.csv"), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        episode_data = generate_reporting_periods(reader)
    rows = remove_duplicates(episode_data)
    rows = remove_rejected(rows)
    rows = filter_unknown_categorised_infective_diagnosis(rows)
    rows = remove_those_who_have_not_completed(rows)
    return rows

if __name__ == "__main__":
    generate_anti_infectives()
