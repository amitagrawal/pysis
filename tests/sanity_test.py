from djangosanetesting.cases import HttpTestCase

class TestSanity(HttpTestCase):

    def test_that_none_of_the_valid_urls_throw_404(self):
        pass

    def test_that_all_pages_are_protected_with_login_required(self):
        pass
