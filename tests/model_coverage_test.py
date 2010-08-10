from django.db.models.loading import get_models, get_apps
from djangosanetesting.cases import DatabaseTestCase

class TestModelCoverage(DatabaseTestCase):
    def test_models(self):
        for app_mod in get_apps():
            app_models = get_models(app_mod)
            for model in app_models:
                assert model.objects.all().count() >= 0, "%s Failed" % model.__name__
