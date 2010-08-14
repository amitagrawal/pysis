from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.views.generic import list_detail
from django.conf import settings
from django.http import HttpResponseRedirect

from myprofile.views import display_my_profile, edit_my_profile

urlpatterns = patterns('',

    (r'^$',
     lambda request: HttpResponseRedirect(settings.MY_PROFILE_LANDING_URL)),

    # Edit My Profile
    url(r'^(?P<category>.*)/edit/$', edit_my_profile,
        name='edit_my_profile'),

    # Display My Profile
    url(r'^(?P<category>.*)/$', display_my_profile,
        name='display_my_profile'),

)
