import datetime
from dateutil.relativedelta import relativedelta
from functools import partial
from six import moves
from opal.models import Episode
from django.db.models import Count, Max
from elcid.models import Diagnosis
from reporting import Report, ReportFile


class IdLiasonReport(Report):
    slug = "id-liason-report"
    display = "ID Liason Report"
    description = "A Monthly Summary of the ID Liason Teams Output"

    def get_queryset(self, month_start):
        month_end = month_start + relativedelta(day=31)
        return Episode.objects.filter(
            tagging__value='id_liaison',
            tagging__archived=True
        ).filter(
            discharge_date__gte=month_start,
            discharge_date__lte=month_end
        )

    def get_age(self, demographics):
        if not demographics.date_of_birth:
            return "Unknown"
        else:
            return relativedelta(
                datetime.date.now(), demographics.date_of_birth
            ).years

    def get_name(self, demographics):
        if demographics.surname:
            if demographics.first_name:
                return "{0} {1}".format(
                    demographics.surname, demographics.first_name
                )
            else:
                return demographics.surname
        else:
            return "Unknown"

    def get_demographics_row(self, episode):
        demographics = episode.patient.demographics_set.first()
        return [
            self.get_name(demographics),
            self.get_age(demographics),
            demographics.sex
        ]

    def get_demographics_headers(self, qs):
        return [
            "Name",
            "Age",
            "Gender"
        ]

    def diagnosis_repetitions(self):
        diagnosis = Diagnosis.objects.filter(episode__in=self.qs)
        diagnosis = diagnosis.annotate(Count('episode_id'))
        return diagnosis.aggregate(Max('episode_id__count'))[
            "episode_id__cont__max"
        ]

    def get_diagnosis_headers(self, qs):
        return [
            "condition_{}".format(i) for i in self.diagnosis_repetitions
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
        qs = episode.clinical_advice_set.all()
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
        result.extend(self.get_clinical_advice_row())
        return result

    def generate_report_data(self, criteria=None, **kwargs):
        month_start = criteria["reporting_month"].format("%d/%m/%Y")

        self.queryset = self.get_queryset(month_start)
        file_data = [self.get_headers()]

        for episode in self.queryset:
            file_data.append(
                self.get_row(episode)
            )

        file_name = "id_liason_report_{0}_{1}.txt".format(
            month_start.month,
            month_start.year
        )

        return [
            ReportFile(
                file_name=file_name, file_data=file_data
            )
        ]
