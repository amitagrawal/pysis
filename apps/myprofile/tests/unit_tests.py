from djangosanetesting.cases import UnitTestCase, DatabaseTestCase, HttpTestCase

class TestSample(UnitTestCase):
    def test_true(self):
        self.assert_true(True)
