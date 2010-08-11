from django.contrib.auth.models import User
from myprofile.models import Profile, Course

username = '09mca001'
password = 'p'

def create_user():
    
    user = User.objects.create_user(username=username,
                                    password=password,
                                    email='a@a.com')

    if len(Profile.objects.all()) == 0:
        c = Course.objects.get(pk=1)
        p = Profile(user=user, course=c, year_of_joining=2009)
        p.save()
    
    return user

