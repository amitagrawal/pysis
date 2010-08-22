from datetime import date
from django_extensions.management.jobs import DailyJob

from accounts.models import Profile
from greetings.greetings_manager import send_birthday_greetings

class Job(DailyJob):
    help = "Sends greetings on Birth Day"

    def execute(self):
        today = date.today()

        todays_birthdays = Profile.objects.filter(actual_date_of_birth__month=today.month,
                                                  actual_date_of_birth__day=today.day)

        for profile in todays_birthdays:
            send_birthday_greetings(profile)
