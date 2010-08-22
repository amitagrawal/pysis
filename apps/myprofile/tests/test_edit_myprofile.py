from djangosanetesting.cases import HttpTestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from accounts.tests import testdata
from accounts.models import Profile, Course


contact_details_url = '/myprofile/contact/edit/'
contact_details = [
    # personal_email_id, personal_contact_number, msg, success?
    ['abcd@abc.com', '99999999999', 'updated successfully', 1],
    ['aaaaa', 'abcd', 'Enter a valid e-mail address', 0],
]

personal_details_url = '/myprofile/personal/edit/'
personal_details = [
    #gender, date_of_birth, actual_date_of_birth, success?
    ['M', '1990-01-01', '1990-1-1', 'updated successfully', 1],
    ['F', '12/8/1998', '12.8.1997', 'updated successfully', 1],
    ['M', '2006/7/23', '1 3 97', 'updated successfully', 1],
    ['M', 'abcd', 'abcd', 'Enter a valid date', 0],
]


class TestMyProfileEdit(HttpTestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.host = 'localhost'
        self.port = 8000

    def setUp(self):
        testdata.run()
        assert self.client.login(username=settings.TEST_USERNAME,
                                 password=settings.TEST_USER_PASSWORD)

    def test_contact_details(self):
        for personal_email_id, personal_contact_number, msg, success in contact_details:

            res = self.client.post(contact_details_url,
                                   {'personal_email_id' : personal_email_id,
                                    'personal_contact_number' : personal_contact_number,
                                   },
                                   follow=True)

            assert msg in res.content

    def test_personal_details(self):
        for gender, date_of_birth, actual_date_of_birth, msg, success in personal_details:
            res = self.client.post(personal_details_url,
                                   {'gender':gender,
                                    'date_of_birth' : date_of_birth,
                                    'actual_date_of_birth' : actual_date_of_birth,
                                   },
                                   follow=True)

            assert msg in res.content
