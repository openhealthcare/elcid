import csv
import os
import dateutil.parser
import copy
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


def get_opat_acceptance():
    rows = []
    with open(get_file_path("location.csv"), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row["opat_acceptance"] or row["opat_acceptance"] == "None":
                row["opat_acceptance"] = None
            else:
                row["opat_acceptance"] = dateutil.parser.parse(row["opat_acceptance"]).date()

            if not row["opat_referral"] or row["opat_referral"] == "None":
                row["opat_referral"] = None
            else:
                row["opat_referral"] = dateutil.parser.parse(row["opat_referral"]).date()
            rows.append(row)
    return rows


def opat_acceptance_union(pid_rows):
    opat_acceptance = get_opat_acceptance()

    for row in pid_rows:
        row.update(get_row_from_episode_id(row["episode_id"], opat_acceptance))
    return pid_rows


def get_lines():
    rows = []
    with open(get_file_path("line.csv"), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row["complications"]:
                row["complications"] = "None"
            rows.append(row)
    return rows


def line_union(pid_rows):
    lines = get_lines()
    result = []

    for line in lines:
        pid_row = get_row_from_episode_id(line["episode_id"], pid_rows)
        if pid_row:
            new_pid_row = copy.copy(pid_row)
            new_pid_row.update(line)
            result.append(new_pid_row)

    return result


def generate_reporting_periods(csv_rows):
    result = []
    # generate reporting period
    for row in csv_rows:
        get_reporting_period(row)
        result.append(row)
    return result


def remove_iv(pid_rows):
    episodes_with_ivs = set()
    with open(get_file_path("antimicrobial.csv"), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        ignore = set(["Inpatient Team", ""])
        rows = [row for row in reader if row["delivered_by"] not in ignore]
        for anitmicrobial_row in rows:
            if anitmicrobial_row["route"] == "IV":
                episodes_with_ivs.add(anitmicrobial_row["episode_id"])
    return [row for row in pid_rows if row["episode_id"] in episodes_with_ivs]


def drugs_union(pid_rows):
    # get episodes ids that had iv and werenot delivered by the inpatient team
    # we then do a union with opat eacceptences
    result = []
    episodes_with_ivs = set()
    with open(get_file_path("antimicrobial.csv"), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        ignore = set(["Inpatient Team", ""])
        rows = [row for row in reader if row["delivered_by"] not in ignore]
        for anitmicrobial_row in rows:
            if anitmicrobial_row["route"] == "IV":
                episodes_with_ivs.add(anitmicrobial_row["episode_id"])

        for row in rows:
            if row["start_date"] and row["end_date"]:
                if not row["end_date"] == "None":
                    if not row["start_date"] == "None":
                        row["start_date"] = dateutil.parser.parse(row["start_date"]).date()
                        row["end_date"] = dateutil.parser.parse(row["end_date"]).date()
                        row["duration"] = (row["end_date"] - row["start_date"]).days + 1

            row["had_iv"] = row["episode_id"] in episodes_with_ivs
            pid_row = get_row_from_episode_id(row["episode_id"], pid_rows)

            if not pid_row or not pid_row["opat_acceptance"]:
                continue

            if "duration" not in row:
                row["duration"] = 0
            else:
                before_opat = (pid_row["opat_acceptance"] - row["start_date"]).days
                row["opat_acceptance"] = pid_row["opat_acceptance"]

                if before_opat > 0:
                    row["duration"] = row["duration"] - before_opat

                if row["duration"] < 0:
                    row["duration"] = 0

            if not row["episode_id"] in episodes_with_ivs:
                continue

            if not row["adverse_event"]:
                row["adverse_event"] = "NA"

            # if they don't have a pid row skip it for the time being
            if pid_row:
                row.update(pid_row)
                result.append(row)

    return result


def group_by(rows, some_fun):
    sliced_data = defaultdict(list)

    for row in rows:
        key = some_fun(row)
        sliced_data[key].append(row)
    return sliced_data


def generate_anti_infectives():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)
    rows = drugs_union(rows)
    rows = [row for row in rows if row["duration"] != 0]

    def get_key(row):
        return (
            # row["duration"],
            row["drug"],
            row["infective_diagnosis"],
            row["reportingperiod"],
        )

    result = []
    sliced_data = group_by(rows, get_key)

    for data_slice_key, value in sliced_data.items():
        counter = str(len(set([i["episode_id"] for i in value])))
        result.append({
            "drug": data_slice_key[0],
            "infective_diagnosis": data_slice_key[1],
            "reportingperiod": data_slice_key[2],
            "duration.max": str(max(v["duration"] for v in value)),
            "count.max": counter
        })

    result.sort(key=lambda x: x["infective_diagnosis"])
    result.sort(key=lambda x: x["drug"])

    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/Anti-infectives by PID and Episodes_ {} .csv"
    )


def compare_files_by_reporting_periods(rows, file_name):
    reporting_periods = list(set(i["reportingperiod"] for i in rows))
    for reporting_period in reporting_periods:
        cut = [i for i in rows if i["reportingperiod"] == reporting_period]
        result = compare_with_file(
            cut,
            file_name.format(reporting_period)
        )

        if result:
            return result


def compare_with_file(result, file_name):
    with open(get_file_path(file_name), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        previous_rows = [previous_row for previous_row in reader]

        if len(previous_rows) != len(result):
            import ipdb; ipdb.set_trace()
        for row_num, row in enumerate(previous_rows):
            if row not in result:
                import ipdb; ipdb.set_trace()


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
    rows = remove_iv(rows)
    rows = filter_unknown_categorised_infective_diagnosis(rows)
    rows = remove_those_who_have_not_completed(rows)
    return rows


def generate_nors_outcomes_po_pid():
    rows = generate_pid()
    rows = remove_iv(rows)
    rows = opat_acceptance_union(rows)

    def get_key(row):
        return (
            row["infective_diagnosis"],
            row["patient_outcome"],
            row["reportingperiod"]
        )
    sliced_data = group_by(rows, get_key)
    result = []
    for key, data in sliced_data.items():
        result.append({
            "infective_diagnosis": key[0],
            "patient_outcome": key[1],
            "reportingperiod": key[2],
            "count.max": str(len(data))
        })
    result.sort(key=lambda x: (x["infective_diagnosis"], x["patient_outcome"],))

    to_append = []
    unsorted_result = result
    result = []
    for row in unsorted_result:
        if row["infective_diagnosis"] == "Other - Free Text":
            to_append.append(row)
        else:
            result.append(row)
    result.extend(to_append)

    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/patient_outcomes_by_diagnosis_ {} .csv"
    )


def generage_nors_outcomes_po_ref():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)

    def get_key(row):
        return (
            row["opat_referral_team"],
            row["patient_outcome"],
            row["reportingperiod"]
        )
    sliced_data = group_by(rows, get_key)
    result = []
    for key, data in sliced_data.items():
        result.append({
            "opat_referral_team": key[0],
            "patient_outcome": key[1],
            "reportingperiod": key[2],
            "count.max": str(len(data))
        })
    result.sort(key=lambda x: (x["opat_referral_team"], x["patient_outcome"],))
    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/patient_outcomes_by_referrer_ {} .csv"
    )


def generate_nors_outcomes_oo_ref():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)

    def get_key(row):
        return (
            row["opat_referral_team"],
            row["opat_outcome"],
            row["reportingperiod"]
        )
    sliced_data = group_by(rows, get_key)
    result = []
    for key, data in sliced_data.items():
        result.append({
            "opat_referral_team": key[0],
            "opat_outcome": key[1],
            "reportingperiod": key[2],
            "count.max": str(len(data))
        })
    result.sort(key=lambda x: (x["opat_referral_team"], x["opat_outcome"],))
    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/opat_outcomes_by_referrer_ {} .csv"
    )


def generate_nors_outcomes_oo_pid():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)

    def get_key(row):
        return (
            row["infective_diagnosis"],
            row["opat_outcome"],
            row["reportingperiod"]
        )
    sliced_data = group_by(rows, get_key)
    result = []
    for key, data in sliced_data.items():
        result.append({
            "infective_diagnosis": key[0],
            "opat_outcome": key[1],
            "reportingperiod": key[2],
            "count.max": str(len(data))
        })
    result.sort(key=lambda x: (x["infective_diagnosis"], x["opat_outcome"],))
    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/opat_outcomes_by_diagnosis_ {} .csv"
    )


def generate_line_adverse_events():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)
    rows = line_union(rows)

    def get_key(row):
        return (
            row["complications"],
            row["reportingperiod"]
        )
    sliced_data = group_by(rows, get_key)
    result = []
    for key, data in sliced_data.items():
        count = str(len(data))
        result.append({
            "complications": key[0],
            "reportingperiod": key[1],
            "count.max": count
        })
    result.sort(key=lambda x: (x["complications"], x["reportingperiod"],))
    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/line_adverse_events_ {} .csv"
    )


def generate_drugs_adverse_events():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)
    rows = drugs_union(rows)
    rows = [row for row in rows if row["duration"] != 0]

    def get_key(row):
        return (
            row["adverse_event"],
            row["reportingperiod"]
        )
    sliced_data = group_by(rows, get_key)
    result = []

    for key, data in sliced_data.items():
        count = str(len(data))
        result.append({
            "adverse_event": key[0],
            "reportingperiod": key[1],
            "count.max": count
        })
    result.sort(key=lambda x: (x["adverse_event"], x["reportingperiod"],))
    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/drug_adverse_events_ {} .csv"
    )


def generate_referring_speciality():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)
    rows = drugs_union(rows)
    rows = [row for row in rows if row["route"] not in ["Oral", "PO"]]

    def get_key(row):
        return (
            row["opat_referral_team"],
            row["reportingperiod"]
        )

    sliced_data = group_by(rows, get_key)
    result = []

    for key, data in sliced_data.items():
        totalopat = sum((i["duration"] for i in data))
        count = len({i["episode_id"] for i in data})
        str(len(data))
        result.append({
            "opat_referral_team": key[0],
            "reportingperiod": key[1],
            "totalopat.max": str(totalopat),
            "count.max": str(count)
        })

    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/Referring Specialty_Patient Episode_Treatment_Days_ {} .csv"
    )


def get_patient(episode_id):
    patient_id = None
    with open(get_file_path("episodes.csv"), "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["id"] == episode_id:
                patient_id = row["patient_id"]

    return patient_id


def get_opat_delivery_statistics():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)
    rows = drugs_union(rows)
    rows = [row for row in rows if row["route"] not in ["Oral", "PO"]]

    def get_key(row):
        return (row["reportingperiod"], row["delivered_by"])

    sliced_data = group_by(rows, get_key)
    result = []

    for key, data in sliced_data.items():
        episodes = str(len(set({i["episode_id"] for i in data})))
        # patients = str(len(set({get_patient(i["episode_id"]) for i in data})))
        durations = sum((i["duration"] for i in data))
        result.append({
            "reportingperiod": key[0],
            "delivered_by": key[1],
            "count.max": episodes,
            "totalopat.max": str(durations),
        })

    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/OPAT Delivery statistics per quarter {} .csv"
    )


def generate_quartersummary():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)
    rows = drugs_union(rows)
    rows = [row for row in rows if row["route"] not in ["Oral", "PO"]]

    def get_key(row):
        return (row["reportingperiod"],)

    sliced_data = group_by(rows, get_key)
    result = []

    for key, data in sliced_data.items():
        episodes = str(len(set({i["episode_id"] for i in data})))
        patients = str(len(set({get_patient(i["episode_id"]) for i in data})))
        durations = sum((i["duration"] for i in data))
        result.append({
            "reportingperiod": key[0],
            "patients.max": patients,
            "episodes.max": str(episodes),
            "treatmentdays.max": str(durations)
        })

    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/Summary statistics per quarter {} .csv"
    )


def generate_primary_infective_diagnosis():
    rows = generate_pid()
    rows = opat_acceptance_union(rows)
    rows = drugs_union(rows)
    rows = [row for row in rows if row["route"] not in ["Oral", "PO"]]

    def get_by_episode(row):
        return (
            row["reportingperiod"],
            row["infective_diagnosis"],
            row["episode_id"]
        )

    def get_key(row):
        return (
            row["reportingperiod"],
            row["infective_diagnosis"],
        )

    sliced_by_episode = group_by(rows, get_by_episode)

    aggregated_by_episode = {}
    for key, data_slice in sliced_by_episode.items():
        aggregated_by_episode[key] = sum(i["duration"] for i in data_slice)

    aggregated_max_duration = defaultdict(int)

    for key, summed_duration in aggregated_by_episode.items():
        aggregated_max_duration[(key[0], key[1],)] = aggregated_max_duration[(key[0], key[1],)] + summed_duration

    sliced_data = group_by(rows, get_key)
    result = []
    for key, data in sliced_data.items():
        episode_count = str(len({i["episode_id"] for i in data}))


        result.append({
            "reportingperiod": key[0],
            "infective_diagnosis": key[1],
            "count.max": episode_count,
            "totalopat.max": str(aggregated_max_duration[key]),
        })
    result.sort(key=lambda x: (x["infective_diagnosis"], x["reportingperiod"],))
    compare_files_by_reporting_periods(
        result,
        "/Users/fredkingham/Downloads/opat_extract/Primary Infective Diagnosis_Patient Episode_Treatment_Days_ {} .csv"
    )


if __name__ == "__main__":
    generate_anti_infectives()

    generate_nors_outcomes_po_pid()
    generage_nors_outcomes_po_ref()
    generate_nors_outcomes_oo_pid()
    generate_nors_outcomes_oo_ref()

    generate_line_adverse_events()
    generate_drugs_adverse_events()

    generate_primary_infective_diagnosis()
    generate_referring_speciality()
    generate_quartersummary()
    get_opat_delivery_statistics()
