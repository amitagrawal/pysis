from datetime import date, timedelta
from django_extensions.management.jobs import DailyJob

from accounts.models import Profile
from greetings.greetings_manager import send_reminder_to_group

class Job(DailyJob):
    help = "Sends a reminder to the group about the upcoming birthdays of its members"

    def execute(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)

        tomorrows_birthdays = Profile.objects.filter(
                                actual_date_of_birth__month=tomorrow.month,
                                actual_date_of_birth__day=tomorrow.day)

        for profile in tomorrows_birthdays:
            send_reminder_to_group(profile)
