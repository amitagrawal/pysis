from djangosanetesting.cases import HttpTestCase
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import mail
from accounts.tests import testdata

class TestResetPassword(HttpTestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.host = 'localhost'
        self.port = 8000

    def setUp(self):
        testdata.run()

    def test_reset_password(self):

        res = self.client.post(reverse('password_reset'),
                               {'register_number' : settings.TEST_USERNAME,
                               },
                               follow=True)

        assert reverse('password_reset_done') in res.request['PATH_INFO']
        assert len(mail.outbox) == 1

        reset_url = [word for word in mail.outbox[0].body.split() if word.startswith('http')][0]
        res = self.client.get(reset_url, follow=True)

        assert res.status_code == 200
        assert 'unsuccessful' not in res.content.lower()
        assert 'change my password' in res.content.lower()

        # I've to stop here, because next step is to change password at Google Apps.
        # Can't mess up production database.
