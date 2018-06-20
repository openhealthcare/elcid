from collections import defaultdict, OrderedDict
from django.db.models import Count, Min, Max
from opal import models as opal_models
from opat import models as opat_models
from opat import quarter_utils
from elcid import models as elcid_models

COMPLETED_THERAPY_STAGE = "Completed Therapy"


def get_iv_route():
    return opal_models.Antimicrobial_route.objects.get(
        name__iexact="IV"
    )


def clean_outcomes(outcomes):
    """
    With opat outcomes we only care about those in the completed state

    Also occasionally we have double clicks.

    We should never have multiple episodes with completed states, but
    we have some double click issues, so we will exclude these.
    """
    outcomes = outcomes.filter(
        outcome_stage=COMPLETED_THERAPY_STAGE
    )

    duplicates = outcomes.values("episode_id").annotate(
        dupe_outcome=Count("episode_id")
    ).filter(dupe_outcome__gt=1)
    to_remove = []
    for duplicate in duplicates:
        repeated = outcomes.filter(episode_id=duplicate["episode_id"])
        repeated = list(repeated.values_list("id", flat=True))[1:]
        to_remove.extend(repeated)

    return outcomes.exclude(id__in=to_remove)


def get_episodes(year, quarter):
    """
    Episodes filtered by start and end date.

    We use the created timestamp, if the created timestamp is
    none, we use the updated timestamp.

    (it shouldn't be but of late but it was possible a few years ago)

    Remove episodes that have not had any IVs

    We exclude episodes that have been rejected
    """
    start_date, end_date = quarter_utils.get_start_end_from_quarter(
        year, quarter
    )
    outcomes = clean_outcomes(opat_models.OPATOutcome.objects.all())
    updated = set(outcomes.filter(
        updated__gte=start_date
    ).filter(
        updated__lte=end_date
    ).filter(created=None).values_list("id", flat=True))

    created = set(outcomes.filter(
        created__gte=start_date
    ).filter(
        created__lte=end_date
    ).values_list("id", flat=True))

    episodes = opal_models.Episode.objects.filter(
        opatoutcome__id__in=created.union(updated)
    ).distinct()

    # remove episodes that have not had any IV
    route = get_iv_route()
    episodes = episodes.filter(antimicrobial__route_fk_id=route.id)

    return episodes.exclude(
        id__in=opat_models.OPATRejection.objects.all().values_list(
            'episode_id', flat=True
        )
    )


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

    drug_start = max(episode_start, antimicrobial.start_date)
    if drug_start and antimicrobial.end_date:
        duration = (antimicrobial.end_date - drug_start).days

        # we are including the end date so we add 1
        duration = duration + 1

        if duration > 0:
            return duration


def print_antimcrobials(year=2017, quarter=2):
    antimicrobials = get_antimicrobials(year, quarter)
    for name, v in antimicrobials.items():
        print "{} {} {}".format(name, v["episodes"], v["duration"])


def aggregate_by_episode_and_drug(drugs):
    episode_id_drug_duration = []

    for drug in drugs:
        drug_name = drug.drug

        if drug.drug_ft:
            drug_name = "Other"
        episode_id_drug_duration.append(
            (drug.episode_id, drug_name, get_drug_duration(drug),)
        )
    return episode_id_drug_duration


def get_antimicrobials(episodes):
    """
    returns a dictionary of
    antimicrobial -> episodes -> episode_count
                  -> duration -> sum(duration)
    """
    drugs = get_relevant_drugs(episodes)
    episode_id_drug_duration = aggregate_by_episode_and_drug(drugs)
    result = defaultdict(lambda: defaultdict(int))
    for episode_id, drug_name, duration in episode_id_drug_duration:
        if duration:
            result[drug_name]["episodes"] += 1
            result[drug_name]["duration"] += duration
    return result


def get_adverse_reactions(episodes):
    line_dict = get_line_reactions(episodes)
    drug_dict = get_drug_reactions(episodes)
    result = {}
    for k, v in line_dict.items():
        result["Line - {}".format(k)] = v

    for k, v in drug_dict.items():
        result["Drug - {}".format(k)] = v
    return result


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

    for episode in episodes:
        outcome = clean_outcomes(episode.opatoutcome_set.all()).get()
        diagnosis_name = "Other"
        if outcome.infective_diagnosis_fk_id:
            diagnosis_name = outcome.infective_diagnosis

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

    result = []
    for diagnosis, result_dict in by_diagnosis.items():
        row = OrderedDict()
        row["diagnosis"] = diagnosis
        row["episode"] = result_dict["episode"]
        row["time_saved"] = result_dict["time_saved"]
        for k, v in result_dict.items():
            if k.startswith("patient_outcome"):
                row[k] = v

        for k, v in result_dict.items():
            if k.startswith("opat_outcome"):
                row[k] = v
        result.append(row)

    return result


def get_summary(episodes):
    result = dict()
    result["total_line_events"] = sum(
        i for i in get_line_reactions(episodes).values()
    )
    result["total_drug_events"] = sum(
        i for i in get_drug_reactions(episodes).values()
    )
    durations = get_iv_duration(episodes)
    result["episodes"] = episodes.count()
    result["total_treatment_days_saved"] = sum(i for i in durations.values())
    return result
