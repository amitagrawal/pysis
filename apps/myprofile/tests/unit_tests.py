from djangosanetesting.cases import UnitTestCase

class TestSample(UnitTestCase):
    def test_true(self):
        self.assert_true(True)
