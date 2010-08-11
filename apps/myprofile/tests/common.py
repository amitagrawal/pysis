
selenium_timeout = '30000'

username = '09mca001'
password = 'p'

def create_user():
    from django.contrib.auth.models import User
    return User.objects.create_user(username=username,
                                    password=password,
                                    email='a@a.com')
