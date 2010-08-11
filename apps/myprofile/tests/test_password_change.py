from djangosanetesting.cases import HttpTestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from common import create_user, username, password

password_change_url = reverse('password_change')
passwords = [
    # old, new, msg, success?
    [password, 'abcdef', 'Successfully changed your password', 1],
    ['some-junk', '123456', 'Your old password was entered incorrectly', 0],
    ['abcdef', password, 'Successfully changed your password', 1],
]

class TestPasswordChange(HttpTestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.host = 'localhost'
        self.port = 8000

    def test_password_change(self):
        user = create_user()
        assert self.client.login(username=username, password=password)
        
        for old, new, msg, success in passwords:
            res = self.client.post(password_change_url,
                                   {'old_password':old,
                                    'new_password1':new,
                                    'new_password2':new,
                                   },
                                   follow=True)

            assert msg in res.content
        
            if success:
                self.client.logout()
                assert self.client.login(username=username, password=new)
