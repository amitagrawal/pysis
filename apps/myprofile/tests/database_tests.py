from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from myprofile.models import Profile, Course
from common import create_user

class TestDatabase(DestructiveDatabaseTestCase):

    def test_profile_creation(self):
        assert len(Profile.objects.all()) == 0

        user = create_user()
        Profile.objects.create(user=user)

        assert len(Profile.objects.all()) == 1


    def test_course_creation(self):
        assert len(Course.objects.all()) == 0

        Course.objects.create(code='mca',
                              name='MCA',
                              duration=3,
                              level='PG')

        assert len(Course.objects.all()) == 1
