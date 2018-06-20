import datetime
from functools import partial
from django.utils.functional import cached_property
from reporting import Report, ReportFile
from opat import nors_utils
from opat import quarter_utils


class NORSReport(Report):
    slug = "nors-report"
    display_name = "OPAT NORs Report"
    description = "A Quarterly summary of the OPAT service"
    template = "reports/opat/nors_report.html"

    def generate_report_data(self, criteria=None, **kwargs):
        quarter_start = criteria["quarter"]  # a string for example 2017_4

        # generated by the value field in reports_available
        year, quarter = quarter_start.split("_")
        episodes = nors_utils.get_episodes(int(year), int(quarter))
        antimicrobials = nors_utils.get_antimicrobials(episodes)
        adverse_reactions = nors_utils.get_adverse_reactions(episodes)
        pid = nors_utils.get_primary_infective_diagnosis(episodes)
        summary = nors_utils.get_summary(episodes)
        fn = partial(self.get_file_name, quarter_start)
        return [
            ReportFile(
                file_name=fn("antimicrobials"),
                file_data=self.flatten_rows_of_dicts(antimicrobials)
            ),
            ReportFile(
                file_name=fn("adverse_reactions"),
                file_data=self.flatten_rows_of_dicts(adverse_reactions)
            ),
            ReportFile(
                file_name=fn("primary_infective_diagnosis"),
                file_data=self.flatten_rows_of_dicts(pid)
            ),
            ReportFile(
                file_name=fn("summary"),
                file_data=self.flatten_rows_of_dicts([summary])
            )
        ]

    def flatten_rows_of_dicts(self, rows_of_dicts):
        """ Flattens out rows of dictionaries into
            something that yields lists of lists.

            We don't use a csv dictwriter because
            we will want to write out some non
            dicts at some point
        """
        if not len(rows_of_dicts):
            yield []
        else:
            headers = rows_of_dicts[0].keys()
            yield headers
            for row in rows_of_dicts:
                yield [row[i] for i in headers]

    def get_file_name(self, quarter_start, some_str):
        return "{}_{}.csv"

    def reports_available(self):
        reports = []
        quarter = quarter_utils.get_quarter_from_date(
            datetime.date.today()
        )

        quarters = []
        for i in xrange(4):
            quarter = quarter_utils.get_previous_quarter(*quarter)
            quarters.append(quarter)

        for year, quarter in quarters:
            start_date, end_date = quarter_utils.get_start_end_from_quarter(
                year, quarter
            )
            episodes = nors_utils.get_episodes(year, quarter)
            reports.append(dict(
                display_name="{}-{}".format(
                    start_date.strftime("%b"),
                    end_date.strftime("%b %Y")
                ),
                report=nors_utils.get_summary(episodes),
                value="{}_{}".format(year, quarter)
            ))

        return reports
