from djangosanetesting.cases import HttpTestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from common import create_user, username, password
from myprofile.models import Profile


general_details_url = '/myprofile/general/edit/'
general_details = [
    # year_of_joining, msg, success?
    ['2009', 'updated successfully', 1],
    ['abcd', 'Enter a number', 0],
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

    def test_general_details(self):
        user = create_user()
        assert self.client.login(username=username, password=password)

        for year, msg, success in general_details:
            res = self.client.post(general_details_url,
                                   {'year_of_joining':year},
                                   follow=True)

            assert msg in res.content
            if success:
                assert int(year) == Profile.objects.get(user=user).year_of_joining

    def test_personal_details(self):
        user = create_user()
        assert self.client.login(username=username, password=password)

        for gender, date_of_birth, actual_date_of_birth, msg, success in personal_details:
            res = self.client.post(personal_details_url,
                                   {'gender':gender,
                                    'date_of_birth':date_of_birth,
                                    'actual_date_of_birth':actual_date_of_birth,
                                   },
                                   follow=True)

            assert msg in res.content