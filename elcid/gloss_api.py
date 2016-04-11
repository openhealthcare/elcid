from django.contrib.auth.models import User
from django.conf import settings
from django.db import transaction

from rest_framework.reverse import reverse

from opal.models import Patient
import requests
import json
import logging


def get_gloss_user():
    user = User.objects.filter(username=settings.GLOSS_USERNAME).first()

    if user:
        return user
    else:
        return User.objects.create(
            username=settings.GLOSS_USERNAME,
            password=settings.GLOSS_PASSWORD
        )


def subscribe(hospital_number):
    base_url = settings.GLOSS_URL_BASE
    url = "{0}/api/subscribe/{1}".format(base_url, hospital_number)
    data = {"end_point": reverse("glossapi-list")}
    response = requests.post(url, data=data)
    assert(response.status_code == 200)


def patient_query(hospital_number, episode):
    base_url = settings.GLOSS_URL_BASE
    url = "{0}/api/patient/{1}".format(base_url, hospital_number)
    response = requests.get(url)

    if not response.status_code == 200:
        logging.error("unable to load patient details for {0} with {1}".format(
            hospital_number, response.status_code
        ))
    else:
        content = json.loads(response.content)

        if content["status"] == "error":
            logging.error(
                "unable to load patient details for {0}, return error {1}").format(
                hospital_number, response["data"]
            )
        else:
            bulk_create_from_gloss_response(content, episode=episode)


def demographics_query(hospital_number):
    base_url = settings.GLOSS_URL_BASE
    url = "{0}/api/demographics/{1}".format(base_url, hospital_number)
    result = json.loads(requests.get(url).content)

    if result["status"] == "success":
        demographics = result["messages"]["demographics"]
        for demographic in demographics:
            demographic["hospital_number"] = hospital_number
            demographic["sourced_from_upstream"] = True

        return [{"demographics": demographics}]
    else:
        # TODO: handle this better
        return []


def bulk_create_from_gloss_response(request_data, episode=None):
    from elcid.models import Allergies

    hospital_number = request_data["hospital_number"]
    update_dict = request_data["messages"]
    logging.info("running a bulk update with")
    logging.info(update_dict)

    if "demographics" not in update_dict:
        update_dict["demographics"] = [
            dict(hospital_number=hospital_number)
        ]

    patient_query = Patient.objects.filter(
        demographics__hospital_number=hospital_number
    )

    if not patient_query.exists():
        patient = Patient()
    else:
        patient = patient_query.get()

    user = get_gloss_user()

    with transaction.atomic():
        if "allergies" in update_dict:
            Allergies.objects.filter(
                patient__demographics__hospital_number=hospital_number
            ).delete()

        patient.bulk_update(update_dict, user, force=True, episode=episode)
