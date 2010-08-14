from djangosanetesting.cases import HttpTestCase
from django.conf import settings

from accounts import testdata

class TestSanity(HttpTestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.host = 'localhost'
        self.port = 8000

        testdata.run()

    def test_that_none_of_the_valid_urls_throw_404(self):
        for page in settings.URLS_TO_TEST:
            res = self.client.get(page, follow=True)
            assert res.status_code != 404, "%s Failed" % page


    def test_that_all_private_urls_are_protected_with_login_required(self):
        for page in settings.URLS_TO_TEST:
            if page not in settings.PUBLIC_URLS:
                res = self.client.get(page, follow=True)
                assert 'Sign in' in res.content, \
                       "%s Failed. Not redirected to Sign in page" % page
                assert res.request['PATH_INFO'] == settings.LOGIN_URL, \
                       "%s Failed. Not redirected to Sign in page" % page


    def test_that_logged_in_user_can_browse_all_urls(self):
        assert self.client.login(username=settings.TEST_USERNAME,
                                 password=settings.TEST_USER_PASSWORD)

        for page in settings.URLS_TO_TEST:
            if page in [settings.LOGIN_URL, settings.LOGIN_URL + '/']:
                continue
            res = self.client.get(page, follow=True)
            assert res.status_code == 200, \
                "%s Failed. Received Status Code = %s" % (page, res.status_code)

            assert 'Sign in' not in res.content, \
                   "%s Failed. Logged in user redirected to Sign in page" % page
            assert res.request['PATH_INFO'] != settings.LOGIN_URL, \
                   "%s Failed. Logged in user redirected to Sign in page" % page

        self.client.logout()
