from datetime import date
from collections import defaultdict
from opal import models as opal_models
from opat import models as opat_models
from elcid import models as elcid_models


def get_quarter_start_end(year, quarter):
    """
    if given a year and a quarter
    return the start/end inclusive
    """
    if quarter == 1:
        start_date = date(year, 1, 1)
        end_date = date(year, 3, 31)
    elif quarter == 2:
        start_date = date(year, 4, 1)
        end_date = date(year, 6, 30)
    elif quarter == 3:
        start_date = date(year, 7, 1)
        end_date = date(year, 9, 30)
    else:
        start_date = date(year, 10, 1)
        end_date = date(year, 12, 31)

    return start_date, end_date


def get_iv_route():
    return opal_models.Antimicrobial_route.objects.get(
        name__iexact="IV"
    )


def get_episodes(start_date, end_date):
    """
    Episodes filtered by start and end date.

    We use the created timestamp, if the created timestamp is
    none, we use the updated timestamp.

    (it shouldn't be but of late but it was possible a few years ago)

    Remove episodes that have not had any IVs

    We exclude episodes that have been rejected
    """
    updated = set(opat_models.OPATOutcome.objects.filter(
        updated__gte=start_date
    ).filter(
        updated__lte=end_date
    ).filter(created=None).values_list("id", flat=True))

    created = set(opat_models.OPATOutcome.objects.filter(
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


def get_breakdown():
    year = 2017
    quarter = 2
    start, end = get_quarter_start_end(year, quarter)
    episodes = get_episodes(start, end)
    drugs = get_relevant_drugs(episodes)
    episode_id_drug_duration = aggregate_by_episode_and_drug(drugs)
    return episode_id_drug_duration


def get_antimicrobials(year, quarter):
    """
    returns a dictionary of
    antimicrobial -> episodes -> episode_count
                  -> druation -> sum(duration)
    """
    start, end = get_quarter_start_end(year, quarter)
    episodes = get_episodes(start, end)
    drugs = get_relevant_drugs(episodes)

    episode_id_drug_duration = aggregate_by_episode_and_drug(drugs)
    result = defaultdict(lambda: defaultdict(int))
    for episode_id, drug_name, duration in episode_id_drug_duration:
        if not duration:
            duration = 0
        result[drug_name]["episodes"] += 1
        result[drug_name]["duration"] += duration
    return result
