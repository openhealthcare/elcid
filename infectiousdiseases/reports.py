import datetime

from dateutil.relativedelta import relativedelta
from django.utils.functional import cached_property
from functools import partial
from six import moves
from opal.models import Episode
from django.db.models import Count, Max
from elcid.models import Diagnosis
from reporting import Report, ReportFile
from infectiousdiseases.patient_lists import InfectiousDiseasesIdLiason


class IdLiasionReport(Report):
    slug = "id-liasion-report"
    display_name = "ID Liasion Report"
    description = "A Monthly Summary of the ID Liasion Teams Output"
    template = "reports/infectiousdiseases/id_liasion_report.html"

    def get_queryset(self, month_start):
        month_end = month_start + relativedelta(day=31)
        return Episode.objects.filter(
            tagging__value=InfectiousDiseasesIdLiason.subtag,
            tagging__archived=True
        ).filter(
            end__gte=month_start,
            end__lte=month_end
        )

    def get_age(self, demographics):
        if not demographics.date_of_birth:
            return ""
        else:
            return relativedelta(
                datetime.date.today(), demographics.date_of_birth
            ).years

    def get_demographics_row(self, episode):
        demographics = episode.patient.demographics_set.first()
        return [
            demographics.name.strip(),
            self.get_age(demographics),
            demographics.sex
        ]

    def get_demographics_headers(self):
        return [
            "Name",
            "Age",
            "Gender"
        ]

    @cached_property
    def diagnosis_repetitions(self):
        diagnosis = Diagnosis.objects.filter(episode__in=self.qs)

        if not diagnosis:
            return 0

        diagnosis = diagnosis.values('episode_id').annotate(Count('episode_id'))
        return diagnosis.aggregate(Max('episode_id__count'))[
            "episode_id__count__max"
        ]

    def get_diagnosis_headers(self):
        return [
            "Condition {}".format(i + 1) for i in range(self.diagnosis_repetitions)
        ]

    def get_diagnosis_row(self, episode):
        row = []
        for diagnosis in episode.diagnosis_set.all():
            row.append(diagnosis.condition)

        row_length = len(row)

        if not row_length == self.diagnosis_repetitions:
            row.extend(
                "" for i in moves.xrange(
                    self.diagnosis_repetitions - row_length
                )
            )
        return row

    def get_clinical_advice_headers(self):
        return [
            "Clinical Advice Given",
            "Infection Control Advice Given",
            "Change In Antibiotic Prescription",
            "Referred To Opat"
        ]

    def get_aggregate_column(self, qs, field):
        return qs.filter(**{field: True}).count()

    def get_clinical_advice_row(self, episode):
        qs = episode.microbiologyinput_set.all()
        aggregate = partial(self.get_aggregate_column, qs)

        return [
            aggregate("clinical_advice_given"),
            aggregate("infection_control_advice_given"),
            aggregate("change_in_antibiotic_prescription"),
            aggregate("referred_to_opat")
        ]

    def get_row(self, episode):
        result = []
        result.extend(self.get_demographics_row(episode))
        result.extend(self.get_diagnosis_row(episode))
        result.extend(self.get_clinical_advice_row(episode))
        return result

    def get_headers(self):
        result = []
        result.extend(self.get_demographics_headers())
        result.extend(self.get_diagnosis_headers())
        result.extend(self.get_clinical_advice_headers())
        return result

    @cached_property
    def reports_available(self):
        """
            A list of lists of available reports for the template
        """
        first_episode = Episode.objects.filter(
            tagging__value=InfectiousDiseasesIdLiason.subtag,
            tagging__archived=True,
        ).exclude(
            end=None
        ).order_by("end").first()

        if not first_episode:
            return None

        first_date = first_episode.end
        today = datetime.date.today()
        first_date = datetime.date(first_date.year, first_date.month, 1)
        rd = relativedelta(today, first_date)
        num = (rd.years * 12) + rd.months

        months = []

        for i in range(num):
            key_date = first_date + relativedelta(months=i)
            months.append(dict(
                display_month=key_date.strftime("%B"),
                display_year=key_date.strftime("%Y"),
                value=key_date.strftime("%d/%m/%Y")
            ))

        months.reverse()
        rows = []

        for i in range(0, len(months), 4):
            rows.append(months[i:i+4])
        return rows

    def generate_report_data(self, criteria=None, **kwargs):
        month_start = datetime.datetime.strptime(
            criteria["reporting_month"], "%d/%m/%Y"
        ).date()

        self.qs = self.get_queryset(month_start)
        file_data = [self.get_headers()]

        for episode in self.qs:
            file_data.append(
                self.get_row(episode)
            )

        file_name = "id_liasion_report_{0}_{1}.csv".format(
            month_start.month,
            month_start.year
        )

        return [
            ReportFile(
                file_name=file_name, file_data=file_data
            )
        ]
