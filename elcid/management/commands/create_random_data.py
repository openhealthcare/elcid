"""
Randomise our admission dates over the last year.
"""
import datetime
import random
import itertools

from django.core.management.base import BaseCommand

from opal.models import Episode, Patient

first_names = [
    "Jane", "James", "Chandeep", "Samantha", "Oliver", "Charlie",
    "Sophie", "Emily", "Lily", "Olivia", "Amelia", "Isabella"
]

last_names = [
    "Smith", "Jones", "Williams", "Taylor", "Brown", "Davies", "Wilson",
    "Brooke", "King", "Patel", "Jameson", "Davidson", "Williams"
]

class PersonGenerator(object):
    """ returns a whole batch of patients with a single episde
        with names, hospital numbers and dates of birth
    """
    def get_names(self, amount):
        patient = Patient()
        first_name = random.choice(first_names)
        second_name = random.choice(second_names)
        return "%s %s" % (first_name, second_name)

    def get_hospital_numbers(self, amount, seed=0):
        template = "00000000"
        numbers = xrange(seed, amount)
        hospital_numbers = []
        for number in numbers:
            hospital_numbers.append("%s%s" % (template[:len(str(number))], number))
        return hospital_numbers

    def get_unique_hospital_numbers(self, amount):
        pass





class Command(BaseCommand):

    def handle(self, *args, **options):
        # create 100 patients, give each between 1-5 episodes
        # over the past 3 years, at least 10 of which have an episode in the
        # last week

        twentyten = datetime.date(2010, 1, 1)

        for e in Episode.objects.filter(date_of_admission__lt=twentyten):
            year = 2014
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            e.date_of_admission = datetime.date(year, month, day)
            e.save()

    def get_names(self, amount):
        patient = Patient()
        first_name = random.choice(first_names)
        second_name = random.choice(second_names)
        return "%s %s" % (first_name, second_name)

        def get_hospital_numbers(self, )

    def create_patients_and_episodes(self):





        names = [i for i in itertools.combinations()]
                self.patient.save()
                self.patient.demographics_set.update(
                    consistency_token="12345678",
                    name="John Smith",
                    hospital_number="AA1111",
                    date_of_birth="1972-06-20",
                )
                self.demographics = self.patient.demographics_set.get()
        pass
