import tempfile
import zipfile
import copy
import calendar
from reporting import Report
from opal.models import Episode
from opal.core.search.extract import generate_csv_files
from opat import models as opat_models
from collections import defaultdict
import dateutil.parser
import os
import csv
import datetime


class OpatReport(Report):
    slug = "opat-report"
    display_name = "OPAT Report"
    description = "Data for the quarterly OPAT report"
    template = "reports/opat/opat_report.html"

    def get_patient(self, episode_id):
        patient_id = None
        with open(self.get_file_path("episodes.csv"), "rb") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row["ID"] == episode_id:
                    patient_id = row["Patient"]

        return patient_id

    def write_csv(self, report_name, list_of_dicts):
        file_name = os.path.join(
            self.to_tmp_file, report_name
        )
        with open(file_name, "w") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=list_of_dicts[0].keys()
            )
            writer.writeheader()
            for dict_row in list_of_dicts:
                writer.writerow(dict_row)
        return file_name

    def get_file_path(self, file_name):
        return os.path.join(self.from_tmp_file, file_name)

    def generate_existing_csv_files(self, user, from_date, to_date):
        episodes = Episode.objects.filter(
            tagging__value="opat",
            location__opat_acceptance__gte=from_date,
            location__opat_acceptance__lt=to_date
        )
        generate_csv_files(self.from_tmp_file, episodes, user)

    def group_by(self, rows, some_fun):
        sliced_data = defaultdict(list)

        for row in rows:
            key = some_fun(row)
            sliced_data[key].append(row)
        return sliced_data

    def get_row_from_episode_id(self, Episode, rows):
        try:
            return next(row for row in rows if row["Episode"] == Episode)
        except StopIteration:
            return

    def get_opat_acceptance(self):
        rows = []
        with open(self.get_file_path("location.csv"), "rb") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if not row["Date Of Acceptance To OPAT"] or row["Date Of Acceptance To OPAT"] == "None":
                    row["Date Of Acceptance To OPAT"] = None
                else:
                    row["Date Of Acceptance To OPAT"] = dateutil.parser.parse(row["Date Of Acceptance To OPAT"]).date()

                if not row["Date Of Referral To OPAT"] or row["Date Of Referral To OPAT"] == "None":
                    row["Date Of Referral To OPAT"] = None
                else:
                    row["Date Of Referral To OPAT"] = dateutil.parser.parse(row["Date Of Referral To OPAT"]).date()
                rows.append(row)
        return rows

    def opat_acceptance_union(self, pid_rows):
        opat_acceptance = self.get_opat_acceptance()

        for row in pid_rows:
            row.update(self.get_row_from_episode_id(row["Episode"], opat_acceptance))
        return pid_rows

    def generate_reporting_periods(self, csv_rows):
        result = []
        # generate reporting period
        for row in csv_rows:
            self.get_reporting_period(row)
            result.append(row)
        return result

    def get_reporting_periods(self):
        """displays data to show reporting periods on the front end"""
        start = None
        for episode in Episode.objects.filter(tagging__value="opat").order_by("location__opat_acceptance"):
            if episode.start:
                start = episode.start
                break

        if not start:
            return []

        first_quarter = ((start.month-1)/3) + 1
        first_year = start.year
        today = datetime.date.today()

        # we will exclude this last quarter
        last_quarter = ((today.month-1)/3) + 1
        last_year = today.year
        result = []

        for year in range(first_year, last_year + 1):
            if year == first_year:
                start = first_quarter
            else:
                start = 1

            for quarter in xrange(start, 5):
                if year == last_year and quarter == last_quarter:
                    break
                else:
                    result.append({
                        "display_name": "{0} - {1} {2}".format(
                            calendar.month_name[((quarter-1)*3+1)],
                            calendar.month_name[((quarter)*3)],
                            year
                        ),
                        "reporting_period": "{0}_{1}".format(year, quarter),
                        "year": year
                    })
        return reversed(result)

    def get_reporting_period(self, pid_row):
        time_field = None
        for field in ["Created", "Updated"]:
            if not time_field and len(pid_row[field].strip()) and not pid_row[field] == "None":
                time_field = dateutil.parser.parse(pid_row[field])

        if not time_field:
            # not sure how to handle these skip them for the mo
            pid_row["reportingperiod"] = "None_NA"
        else:
            year = time_field.year
            quarter = ((time_field.month -1) / 3) + 1
            pid_row["reportingperiod"] = "{0}_{1}".format(year, quarter)

    def remove_duplicates(self, rows):
        result = {}
        for row in rows:
            key = (row["Episode"], row["Outcome Stage"],)
            if key not in result:
                result[key] = row

        return result.values()

    def remove_rejected(self, rows):
        episode_ids = set()
        file_name = self.get_file_path("opat_rejection.csv")
        if not os.path.exists(file_name):
            return rows
        else:
            with open(file_name, "rb") as csv_file:
                reader = csv.DictReader(csv_file)
                episode_ids = {i["Episode"] for i in reader}
            return [i for i in rows if i["Episode"] not in episode_ids]

    def remove_iv(self, pid_rows):
        episodes_with_ivs = set()
        with open(self.get_file_path("antimicrobial.csv"), "rb") as csv_file:
            reader = csv.DictReader(csv_file)
            ignore = set(["Inpatient Team", ""])
            rows = [row for row in reader if row["Delivered By"] not in ignore]
            for anitmicrobial_row in rows:
                if anitmicrobial_row["Route"] == "IV":
                    episodes_with_ivs.add(anitmicrobial_row["Episode"])
        return [row for row in pid_rows if row["Episode"] in episodes_with_ivs]

    def filter_unknown_categorised_infective_diagnosis(self, rows):
        for row in rows:
            if row["Infective Diagnosis"]:
                qs = opat_models.OPATInfectiveDiagnosis.objects.filter(
                    name=row["Infective Diagnosis"]
                )
                if qs.exists():
                    continue
            row["Infective Diagnosis"] = "Other - Free Text"

        return rows

    def remove_those_who_have_not_completed(self, rows):
        return [
            row for row in rows if row["Outcome Stage"] == "Completed Therapy"
        ]

    def generate_pid(self):
        rows = []
        with open(self.get_file_path("opat_outcome.csv"), "rb") as csv_file:
            reader = csv.DictReader(csv_file)
            episode_data = self.generate_reporting_periods(reader)
        rows = self.remove_duplicates(episode_data)
        rows = self.remove_rejected(rows)
        rows = self.remove_iv(rows)
        rows = self.filter_unknown_categorised_infective_diagnosis(rows)
        rows = self.remove_those_who_have_not_completed(rows)
        return rows

    def get_lines(self):
        rows = []
        with open(self.get_file_path("line.csv"), "rb") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if not row["Complications"]:
                    row["Complications"] = "None"
                rows.append(row)
        return rows

    def line_union(self, pid_rows):
        lines = self.get_lines()
        result = []

        for line in lines:
            pid_row = self.get_row_from_episode_id(line["Episode"], pid_rows)
            if pid_row:
                new_pid_row = copy.copy(pid_row)
                new_pid_row.update(line)
                result.append(new_pid_row)

        return result

    def reporting_period_to_date_range(self, reporting_period):
        """ The reporting period is of the form 1_
        """

    def drugs_union(self, pid_rows):
        # get episodes ids that had iv and werenot delivered by the inpatient team
        # we then do a union with opat eacceptences
        result = []
        episodes_with_ivs = set()
        with open(self.get_file_path("antimicrobial.csv"), "rb") as csv_file:
            reader = csv.DictReader(csv_file)
            ignore = set(["Inpatient Team", ""])
            rows = [row for row in reader if row["Delivered By"] not in ignore]
            for anitmicrobial_row in rows:
                if anitmicrobial_row["Route"] == "IV":
                    episodes_with_ivs.add(anitmicrobial_row["Episode"])

            for row in rows:
                if row["Start Date"] and row["End Date"]:
                    if not row["End Date"] == "None":
                        if not row["Start Date"] == "None":
                            row["Start Date"] = dateutil.parser.parse(row["Start Date"]).date()
                            row["End Date"] = dateutil.parser.parse(row["End Date"]).date()
                            row["Duration"] = (row["End Date"] - row["Start Date"]).days + 1

                row["had_iv"] = row["Episode"] in episodes_with_ivs
                pid_row = self.get_row_from_episode_id(row["Episode"], pid_rows)

                if not pid_row or not pid_row["Date Of Acceptance To OPAT"]:
                    continue

                if "Duration" not in row:
                    row["Duration"] = 0
                else:
                    before_opat = (pid_row["Date Of Acceptance To OPAT"] - row["Start Date"]).days
                    row["Date Of Acceptance To OPAT"] = pid_row["Date Of Acceptance To OPAT"]

                    if before_opat > 0:
                        row["Duration"] = row["Duration"] - before_opat

                    if row["Duration"] < 0:
                        row["Duration"] = 0

                if not row["Episode"] in episodes_with_ivs:
                    continue

                if not row["Adverse Event"]:
                    row["Adverse Event"] = "NA"

                # if they don't have a pid row skip it for the time being
                if pid_row:
                    row.update(pid_row)
                    result.append(row)

        return result

    def generate_anti_infectives(self, reporting_period):
        file_name = "Anti-infectives by PID and Episodes_ {} .csv".format(
            reporting_period
        )
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)
        rows = self.drugs_union(rows)
        rows = [row for row in rows if row["Duration"] != 0]

        def get_key(row):
            return (
                # row["Duration"],
                row["Drug"],
                row["Infective Diagnosis"],
                row["reportingperiod"],
            )

        result = []
        sliced_data = self.group_by(rows, get_key)

        for data_slice_key, value in sliced_data.items():
            if data_slice_key[2] == reporting_period:
                counter = str(len(set([i["Episode"] for i in value])))
                result.append({
                    "Drug": data_slice_key[0],
                    "Infective Diagnosis": data_slice_key[1],
                    "reportingperiod": data_slice_key[2],
                    "Duration.max": str(max(v["Duration"] for v in value)),
                    "count.max": counter
                })

        return (self.write_csv(file_name, result), file_name,)

    def generage_nors_outcomes_po_ref(self, reporting_period):
        file_name = "patient_outcomes_by_referrer_ {} .csv".format(
            reporting_period
        )
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)

        def get_key(row):
            return (
                row["Referring Team"],
                row["Patient Outcome"],
                row["reportingperiod"]
            )
        sliced_data = self.group_by(rows, get_key)
        result = []
        for key, data in sliced_data.items():
            if key[2] == reporting_period:
                result.append({
                    "Referring Team": key[0],
                    "Patient Outcome": key[1],
                    "reportingperiod": key[2],
                    "count.max": str(len(data))
                })
        result.sort(key=lambda x: (x["Referring Team"], x["Patient Outcome"],))
        return (self.write_csv(file_name, result), file_name,)

    def generate_nors_outcomes_oo_ref(self, reporting_period):
        file_name = "opat_outcomes_by_referrer_ {} .csv".format(
            reporting_period
        )
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)

        def get_key(row):
            return (
                row["Referring Team"],
                row["Opat Outcome"],
                row["reportingperiod"]
            )
        sliced_data = self.group_by(rows, get_key)
        result = []
        for key, data in sliced_data.items():
            if key[2] == reporting_period:
                result.append({
                    "Referring Team": key[0],
                    "Opat Outcome": key[1],
                    "reportingperiod": key[2],
                    "count.max": str(len(data))
                })
        result.sort(key=lambda x: (x["Referring Team"], x["Opat Outcome"],))
        return (self.write_csv(file_name, result), file_name,)

    def generate_nors_outcomes_oo_pid(self, reporting_period):
        file_name = "opat_outcomes_by_diagnosis_ {} .csv".format(
            reporting_period
        )
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)

        def get_key(row):
            return (
                row["Infective Diagnosis"],
                row["Opat Outcome"],
                row["reportingperiod"]
            )
        sliced_data = self.group_by(rows, get_key)
        result = []
        for key, data in sliced_data.items():
            if key[2] == reporting_period:
                result.append({
                    "Infective Diagnosis": key[0],
                    "Opat Outcome": key[1],
                    "reportingperiod": key[2],
                    "count.max": str(len(data))
                })
        result.sort(key=lambda x: (x["Infective Diagnosis"], x["Opat Outcome"],))
        return (self.write_csv(file_name, result), file_name,)

    def generate_nors_outcomes_po_pid(self, reporting_period):
        file_name = "patient_outcomes_by_diagnosis_ {} .csv".format(
            reporting_period
        )
        rows = self.generate_pid()
        rows = self.remove_iv(rows)
        rows = self.opat_acceptance_union(rows)

        def get_key(row):
            return (
                row["Infective Diagnosis"],
                row["Patient Outcome"],
                row["reportingperiod"]
            )
        sliced_data = self.group_by(rows, get_key)
        result = []
        for key, data in sliced_data.items():
            if key[2] == reporting_period:
                result.append({
                    "Infective Diagnosis": key[0],
                    "Patient Outcome": key[1],
                    "reportingperiod": key[2],
                    "count.max": str(len(data))
                })
        result.sort(key=lambda x: (x["Infective Diagnosis"], x["Patient Outcome"],))

        return (self.write_csv(file_name, result), file_name,)

    def generate_line_adverse_events(self, reporting_period):
        file_name = "line_adverse_events_ {} .csv".format(
            reporting_period
        )
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)
        rows = self.line_union(rows)

        def get_key(row):
            return (
                row["Complications"],
                row["reportingperiod"]
            )
        sliced_data = self.group_by(rows, get_key)
        result = []
        for key, data in sliced_data.items():
            if key[1] == reporting_period:
                count = str(len(data))
                result.append({
                    "Complications": key[0],
                    "reportingperiod": key[1],
                    "count.max": count
                })
        result.sort(key=lambda x: (x["Complications"], x["reportingperiod"],))
        return (self.write_csv(file_name, result), file_name,)

    def generate_drugs_adverse_events(self, reporting_period):
        file_name = "drug_adverse_events_ {} .csv".format(
            reporting_period
        )
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)
        rows = self.drugs_union(rows)
        rows = [row for row in rows if row["Duration"] != 0]

        def get_key(row):
            return (
                row["Adverse Event"],
                row["reportingperiod"]
            )
        sliced_data = self.group_by(rows, get_key)
        result = []

        for key, data in sliced_data.items():
            if key[1] == reporting_period:
                count = str(len(data))
                result.append({
                    "Adverse Event": key[0],
                    "reportingperiod": key[1],
                    "count.max": count
                })
        result.sort(key=lambda x: (x["Adverse Event"], x["reportingperiod"],))
        return (self.write_csv(file_name, result), file_name,)

    def generate_primary_infective_diagnosis(self, reporting_period):
        fn = "Primary Infective Diagnosis_Patient Episode_Treatment_Days_ {} .csv"
        file_name = fn.format(
            reporting_period
        )
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)
        rows = self.drugs_union(rows)
        rows = [row for row in rows if row["Route"] not in ["Oral", "PO"]]

        def get_by_episode(row):
            return (
                row["reportingperiod"],
                row["Infective Diagnosis"],
                row["Episode"]
            )

        def get_key(row):
            return (
                row["reportingperiod"],
                row["Infective Diagnosis"],
            )

        sliced_by_episode = self.group_by(rows, get_by_episode)

        aggregated_by_episode = {}
        for key, data_slice in sliced_by_episode.items():
            aggregated_by_episode[key] = sum(i["Duration"] for i in data_slice)

        aggregated_max_duration = defaultdict(int)

        for key, summed_duration in aggregated_by_episode.items():
            aggregated_max_duration[(key[0], key[1],)] = aggregated_max_duration[(key[0], key[1],)] + summed_duration

        sliced_data = self.group_by(rows, get_key)
        result = []
        for key, data in sliced_data.items():
            episode_count = str(len({i["Episode"] for i in data}))
            if key[0] == reporting_period:
                result.append({
                    "reportingperiod": key[0],
                    "Infective Diagnosis": key[1],
                    "count.max": episode_count,
                    "totalopat.max": str(aggregated_max_duration[key]),
                })
        result.sort(
            key=lambda x: (x["Infective Diagnosis"], x["reportingperiod"],)
        )
        return (self.write_csv(file_name, result), file_name,)

    def generate_referring_speciality(self, reporting_period):
        fn = "Referring Specialty_Patient Episode_Treatment_Days_ {} .csv"
        file_name = fn.format(reporting_period)
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)
        rows = self.drugs_union(rows)
        rows = [row for row in rows if row["Route"] not in ["Oral", "PO"]]

        def get_key(row):
            return (
                row["Referring Team"],
                row["reportingperiod"]
            )

        sliced_data = self.group_by(rows, get_key)
        result = []

        for key, data in sliced_data.items():
            if key[1] == reporting_period:
                totalopat = sum((i["Duration"] for i in data))
                count = len({i["Episode"] for i in data})
                str(len(data))
                result.append({
                    "Referring Team": key[0],
                    "reportingperiod": key[1],
                    "totalopat.max": str(totalopat),
                    "count.max": str(count)
                })
        return (self.write_csv(file_name, result), file_name,)

    def generate_quartersummary(self, reporting_period):
        file_name = "Summary statistics per quarter {} .csv".format(reporting_period)
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)
        rows = self.drugs_union(rows)
        rows = [row for row in rows if row["Route"] not in ["Oral", "PO"]]

        def get_key(row):
            return (row["reportingperiod"],)

        sliced_data = self.group_by(rows, get_key)
        result = []

        for key, data in sliced_data.items():
            if key[0] == reporting_period:
                episodes = str(len(set({i["Episode"] for i in data})))
                patients = str(len(set({self.get_patient(i["Episode"]) for i in data})))
                durations = sum((i["Duration"] for i in data))
                result.append({
                    "reportingperiod": key[0],
                    "patients.max": patients,
                    "episodes.max": str(episodes),
                    "treatmentdays.max": str(durations)
                })

        return (self.write_csv(file_name, result), file_name,)

    def get_opat_delivery_statistics(self, reporting_period):
        file_name = "OPAT Delivery statistics per quarter {} .csv".format(
            reporting_period
        )
        rows = self.generate_pid()
        rows = self.opat_acceptance_union(rows)
        rows = self.drugs_union(rows)
        rows = [row for row in rows if row["Route"] not in ["Oral", "PO"]]

        def get_key(row):
            return (row["reportingperiod"], row["Delivered By"])

        sliced_data = self.group_by(rows, get_key)
        result = []

        for key, data in sliced_data.items():
            if key[0] == reporting_period:
                episodes = str(len(set({i["Episode"] for i in data})))
                durations = sum((i["Duration"] for i in data))
                result.append({
                    "reportingperiod": key[0],
                    "Delivered By": key[1],
                    "count.max": episodes,
                    "totalopat.max": str(durations),
                })

        return (self.write_csv(file_name, result), file_name,)

    def get_date_range_from_reporting_period(self, reporting_period):
        """ returns from date(inc) to date (exc) from a reporting period
        """
        year, quarter = reporting_period.split("_")
        year = int(year)
        quarter = int(quarter)
        month = ((quarter-1) * 3) + 1
        from_date = datetime.date(year, month, 1)

        to_month = month + 3
        if to_month > 12:
            to_month = to_month % 12
            year += 1
        to_date = datetime.date(year, to_month, 1)
        return from_date, to_date

    def zip_archive_report_data(self, user=None, criteria=None):
        self.from_tmp_file = tempfile.mkdtemp()

        self.to_tmp_file = tempfile.mkdtemp()
        from_date, to_date = self.get_date_range_from_reporting_period(
            criteria["reporting_period"]
        )
        self.generate_existing_csv_files(user, from_date, to_date)
        reporting_period = criteria["reporting_period"]

        reports = [
            self.generate_anti_infectives(reporting_period),
            self.generate_nors_outcomes_po_pid(reporting_period),
            self.generage_nors_outcomes_po_ref(reporting_period),
            self.generate_nors_outcomes_oo_pid(reporting_period),
            self.generate_nors_outcomes_oo_ref(reporting_period),
            self.generate_line_adverse_events(reporting_period),
            self.generate_drugs_adverse_events(reporting_period),
            self.generate_primary_infective_diagnosis(reporting_period),
            self.generate_referring_speciality(reporting_period),
            self.generate_quartersummary(reporting_period),
            self.get_opat_delivery_statistics(reporting_period)
        ]

        target = os.path.join(self.to_tmp_file, "opat_report.zip")

        with zipfile.ZipFile(target, mode="w") as z:
            zipfolder = '{0}.{1}.{2}.{3}'.format(
                self.slug,
                user.username,
                datetime.date.today(),
                reporting_period
            )

            for full_file_name, file_name in reports:
                z.write(
                    full_file_name,
                    os.path.join(zipfolder, file_name)
                )
        return target
