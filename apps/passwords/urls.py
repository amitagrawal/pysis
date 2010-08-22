from django.conf.urls.defaults import *
from django.conf import settings
from django.http import HttpResponseRedirect

from passwords.views import password_reset
from passwords.forms import PasswordSelectForm

urlpatterns = patterns('',

    url(r'^change/$',
        lambda request: HttpResponseRedirect(settings.PASSWORD_CHANGE_URL),
        name='password_change'),

    url(r'^reset/$',
        password_reset,
        name='password_reset'),
    url(r'^reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name' : 'passwords/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'set_password_form' : PasswordSelectForm},
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),

)
