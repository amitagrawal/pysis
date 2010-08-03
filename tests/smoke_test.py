## initially a quick smoke test to see if certain URLs throw exceptions or not
## would have caught a high percentage of recent trunk breakages

from djangosanetesting.cases import HttpTestCase

pages = [
    '/',
    '/admin/',
    #'/profiles/',
    #'/announcements/',
    #'/account/login/',
]

class TestSmoke(HttpTestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.host = 'localhost'
        self.port = 8000

    def test_pages(self):
        for page in pages:
            res = self.client.get(page)
            assert res.status_code == 200, "%s Failed" % page
