from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.views.generic import list_detail
from django.conf import settings

from myprofile.views import display_my_profile, edit_my_profile

urlpatterns = patterns('',

    #(r'^$', display_my_profile),

    # Edit my Profile
    url(r'^(?P<category>.*)/edit/$', edit_my_profile, 
        name='edit_my_profile'),
    
    # My Profile
    url(r'^(?P<category>.*)/$', display_my_profile,
        name='display_my_profile'),


    #(r'^search/all/$', display_all_students),
    #(r'^display/(?P<username>.*)/$', display_profile),
    
)    