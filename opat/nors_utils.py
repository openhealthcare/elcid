import logging
from collections import defaultdict, OrderedDict
from django.db.models import Count, Min, Max
from opal import models as opal_models
from opat import models as opat_models
from opat import quarter_utils
from elcid import models as elcid_models
from functools import wraps
from time import time


COMPLETED_THERAPY_STAGE = "Completed Therapy"


BACTERAEMIA = "bacteraemia / blood stream infection / septicaemia"

# NORS translatinos
INFECTIVE_DIAGNOSIS = {
    "bacteraemia": BACTERAEMIA,
    "early onset sepsis": BACTERAEMIA,
    "fever in early infancy": BACTERAEMIA,
    "late onset sepsis": BACTERAEMIA,
    "congenital cmv": "citomegalovirus",
    "hepatic abscess": "intraabdominal abscess",
    "neonatal hsv": "other",
}

ANTIMICROBIALS = {
    "fucidin": "fusidic acid",
    "fusidic": "fusidic acid",
    "piperacillintazobactam": "piperacillin/tazobactam", # we should update this one
    "tigecycline": "tigcycline", # NORS typo
    "tobramycin": "tobramyci", # NORS typo
    "ampicillin": "amoxicillin",
    "cefotaxime": "ceftriaxone",
    "cloxacillin": "flucloxacillin",
    "foscarnet": "other",
    "ganciclovir": "other",
    "peg-interferon": "other",
    "penicillin": "other",
    "piperacillin": "piperacillin/tazobactam",
    "piperacillin tazobactam": "piperacillin/tazobactam",
    "synercid": "other",
    "ticarcillin": "other",
    "tigecycline": "tigcycline" #NORS Typo,
}

logger = logging.getLogger('elcid.time_logger')


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logging.error('timing_func: %r %2.4f sec' % (
            f.__name__, te-ts
        ))
        logging.error('%s len: %s' % (
            f.__name__, len(result)
        ))

        return result
    return wrap


def get_iv_route():
    return opal_models.Antimicrobial_route.objects.get(
        name__iexact="IV"
    )


def clean_outcomes(outcomes):
    outcomes = outcomes.filter(
        outcome_stage=COMPLETED_THERAPY_STAGE
    )
    min_ids = outcomes.values("episode_id").annotate(
        min_id=Min("id")
    ).values_list("min_id", flat=True)
    return outcomes.filter(id__in=min_ids)


def get_episodes():
    outcomes = clean_outcomes(opat_models.OPATOutcome.objects.all())
    episodes = opal_models.Episode.objects.filter(
        id__in=outcomes.values_list("episode_id").distinct()
    )
    return episodes.exclude(
        id__in=opat_models.OPATRejection.objects.all().values_list(
            'episode_id', flat=True
        )
    )


def get_iv_antimicrobials(episodes):
    route = get_iv_route()
    return get_relevant_drugs(episodes).filter(
        route_fk_id=route.id
    ).exclude(
        end_date=None
    ).values("episode_id").annotate(max_end=Max("end_date"))


def get_episodes_for_quarters(
    quarters
):
    episodes = get_episodes()
    antimicrobials = get_iv_antimicrobials(episodes)
    episode_id_to_max_date = {
        i["episode_id"]: i["max_end"] for i in antimicrobials
    }

    quarter_to_episode_id = defaultdict(list)
    for episode_id, max_date in episode_id_to_max_date.items():
        quarter = quarter_utils.Quarter.from_date(max_date)
        quarter_to_episode_id[quarter].append(episode_id)

    result = dict()
    for quarter in quarters:
        result[quarter] = opal_models.Episode.objects.filter(
            id__in=quarter_to_episode_id[quarter]
        )

    return result


def filter_episodes_by_quarter(
    episodes, antimicrobials, quarter
):
    antimicrobials = antimicrobials.filter(max_end__gte=quarter.start)
    antimicrobials = antimicrobials.filter(max_end__lte=quarter.end)
    return episodes.filter(
        id__in=antimicrobials.values_list("episode_id", flat=True).distinct()
    )


@timing
def get_episodes_for_quarter(quarter):
    """
    Episodes filtered by start and end date.

    We use the created timestamp, if the created timestamp is
    none, we use the updated timestamp.

    (it shouldn't be but of late but it was possible a few years ago)

    Remove episodes that have not had any IVs

    We exclude episodes that have been rejected
    """
    episodes = get_episodes()
    route = get_iv_route()
    antimicrobials = get_relevant_drugs(episodes).filter(
        route_fk_id=route.id
    ).values("episode_id").annotate(max_end=Max("end_date"))
    return filter_episodes_by_quarter(episodes, antimicrobials, quarter)


def get_relevant_drugs(episodes):
    delivered_by = elcid_models.Drug_delivered.objects.filter(
        name="Inpatient Team"
    )

    if not delivered_by.exists():
        raise ValueError("Unable to find inpatient team")

    antimicrobials = elcid_models.Antimicrobial.objects.filter(
        episode__in=episodes
    ).exclude(
        delivered_by_fk_id=delivered_by.get()
    )

    # if delivered by is not filled in exclude it
    to_ignore = antimicrobials.filter(
        delivered_by_fk_id=None
    ).filter(
        delivered_by_ft=""
    ).values_list("id", flat=True)

    antimicrobials = antimicrobials.exclude(
        id__in=to_ignore
    )

    return antimicrobials


def get_drug_duration(antimicrobial):
    """
    get drug duration, but only for the time
    they are actually on opat.
    """
    if not antimicrobial.start_date:
        return

    episode = antimicrobial.episode
    episode_start = episode.start

    if not episode_start:
        location = episode.location_set.first()
        episode_start = location.opat_acceptance

        if not episode_start:
            episode_start = location.opat_referral

    if episode_start and antimicrobial.start_date:
        drug_start = max(episode_start, antimicrobial.start_date)
    else:
        drug_start = episode_start or antimicrobial.start_date

    if drug_start and antimicrobial.end_date:
        duration = (antimicrobial.end_date - drug_start).days

        # we are including the end date so we add 1
        duration = duration + 1

        if duration > 0:
            return duration


def get_drug_name(drug):
    drug_name = drug.drug.lower()

    if drug_name in ANTIMICROBIALS:
        return ANTIMICROBIALS[drug_name]

    if drug.drug_ft:
        drug_name = "other"
    return drug_name


def get_antimicrobials(episodes):
    drugs = get_relevant_drugs(episodes)
    result = defaultdict(lambda: defaultdict(int))

    for drug in drugs:
        drug_name = get_drug_name(drug)
        duration = get_drug_duration(drug)
        if duration:
            result[drug_name]["episodes"] += 1
            result[drug_name]["duration"] += duration
            result[drug_name][drug.delivered_by] += 1
    return result


def get_antimicrobial_report(episodes):
    antimicrobials = get_antimicrobials(episodes)
    result = []

    # delivered by is a select box so we don't need to worry about
    # free text
    delivered_by = elcid_models.Drug_delivered.objects.values_list(
        "name", flat=True
    ).order_by("name")
    for drug_name, drug_dict in antimicrobials.items():
        row = OrderedDict(antimicrobial=drug_name)
        row["episodes"] = drug_dict["episodes"]
        row["duration"] = drug_dict["duration"]
        for d in delivered_by:
            row[d] = drug_dict.get(d, 0)
        result.append(row)
    return result


def get_adverse_reactions(episodes):
    line_dict = get_line_reactions(episodes)
    drug_dict = get_drug_reactions(episodes)
    result = {}
    for k, v in line_dict.items():
        result["Line - {}".format(k)] = v

    for k, v in drug_dict.items():
        result["Drug - {}".format(k)] = v
    if result:
        return [result]
    return []


def get_ft_or_fk_coded_count(qs, field_name, fk_model):
    fk_id = "{}_fk_id".format(field_name)
    ft_name = "{}_ft".format(field_name)
    coded_qs = qs.exclude(**{fk_id: None})
    counted_rows = coded_qs.values(fk_id).annotate(
        coded_count=Count(fk_id)
    )
    result = dict()

    for counted_row in counted_rows:
        fk_name = fk_model.objects.get(id=counted_row[fk_id]).name
        result[fk_name] = counted_row["coded_count"]

    other = qs.filter(**{fk_id: None}).exclude(**{ft_name: ''})

    # occasionally people put `none` as the adverse event, lets
    # skip those
    other_count = other.exclude(
        **{ft_name: None}
    ).exclude(**{"{}__iexact".format(ft_name): "none"}).count()

    if other_count:
        result["Other"] = other_count
    return result


def get_line_reactions(episodes):
    lines = elcid_models.Line.objects.filter(episode__in=episodes)
    return get_ft_or_fk_coded_count(
        lines, "complications", opal_models.Line_complication
    )


def get_drug_reactions(episodes):
    drugs = get_relevant_drugs(episodes)
    return get_ft_or_fk_coded_count(
        drugs, "adverse_event", opal_models.Antimicrobial_adverse_event
    )


def get_iv_duration(episodes):
    """
    returns the max length of iv during an episode
    """
    iv_route = get_iv_route()
    drugs = get_relevant_drugs(episodes)
    drugs.filter(route_fk_id=iv_route.id)

    drugs = drugs.values("episode_id").annotate(
        min_start_date=Min("start_date"),
        max_end_date=Max("end_date")
    )
    result = {}
    for i in drugs:
        if i["max_end_date"] and i["min_start_date"]:
            diff = (i["max_end_date"] - i["min_start_date"]).days
            diff += 1
            diff = max(diff, 0)
            result[i["episode_id"]] = diff
    return result


def get_primary_infective_diagnosis(episodes):
    by_diagnosis = defaultdict(
        lambda: defaultdict(int)
    )

    episode_to_iv_duration = get_iv_duration(episodes)

    # a list of all the outcomes as we expect the table
    # to include all outcomes as headers
    outcomes = set()

    for episode in episodes:
        outcome = clean_outcomes(episode.opatoutcome_set.all()).get()
        diagnosis_name = "other"
        if outcome.infective_diagnosis_fk_id:
            diagnosis_name = outcome.infective_diagnosis.lower()

        diagnosis_name = INFECTIVE_DIAGNOSIS.get(
            diagnosis_name, diagnosis_name
        )

        opat_outcome = outcome.opat_outcome
        patient_outcome = outcome.patient_outcome
        by_diagnosis[diagnosis_name]["episode"] += 1
        by_diagnosis[diagnosis_name]["time_saved"] += episode_to_iv_duration.get(
            episode.id, 0
        )

        patient_outcome_key = "patient_outcome__{}".format(
            patient_outcome
        )
        by_diagnosis[diagnosis_name][patient_outcome_key] += 1
        opat_outcome_key = "opat_outcome__{}".format(
            opat_outcome
        )
        by_diagnosis[diagnosis_name][opat_outcome_key] += 1
        outcomes.add(patient_outcome_key)
        outcomes.add(opat_outcome_key)

    result = []
    outcomes = sorted(list(outcomes))
    for diagnosis, result_dict in by_diagnosis.items():
        row = OrderedDict()
        row["diagnosis"] = diagnosis
        row["episode"] = result_dict["episode"]
        row["time_saved"] = result_dict["time_saved"]
        for outcome in outcomes:
            if outcome not in result_dict:
                row[outcome] = 0
            else:
                row[outcome] = result_dict[outcome]
        result.append(row)

    return result


def get_num_episodes_rejected(quarter):
    return opat_models.OPATRejection.objects.filter(
        date__lte=quarter.start, date__gte=quarter.end
    ).values_list('episode_id', flat=True).distinct().count()


def get_summary(episodes, quarter):
    result = OrderedDict()
    result["episodes"] = episodes.count()
    result["episodes_rejected"] = get_num_episodes_rejected(quarter)
    durations = get_iv_duration(episodes)
    result["total_treatment_days_saved"] = sum(durations.values())
    result["total_line_events"] = sum(
        i for i in get_line_reactions(episodes).values()
    )
    result["total_drug_events"] = sum(
        i for i in get_drug_reactions(episodes).values()
    )
    return result
