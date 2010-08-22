from datetime import date, timedelta
from djangosanetesting.cases import HttpTestCase
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import mail
from accounts.tests import testdata
from accounts.models import Profile

class TestGreetings(HttpTestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.host = 'localhost'
        self.port = 8000

    def setUp(self):
        testdata.run()

    def test_birthday_greetings(self):
        today = date.today()
        profile = Profile.objects.get(user__username=settings.TEST_USERNAME)
        profile.actual_date_of_birth = today
        profile.save()

        assert len(mail.outbox) == 0

        from greetings.jobs.daily.birthday_greetings import Job
        job = Job()
        job.execute()

        assert len(mail.outbox) == 1
        assert 'Happy Birthday' in mail.outbox[0].body
        assert profile.college_email_id in mail.outbox[0].to


    def test_birthday_reminders(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        profile = Profile.objects.get(user__username=settings.TEST_USERNAME)
        profile.actual_date_of_birth = tomorrow
        profile.save()

        assert len(mail.outbox) == 0

        from greetings.jobs.daily.birthday_reminders import Job
        job = Job()
        job.execute()

        assert len(mail.outbox) == 1
        assert profile.register_number in mail.outbox[0].body
