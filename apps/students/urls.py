from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.views.generic import list_detail
from django.conf import settings
from django.http import HttpResponseRedirect

from students.views import search_profiles, display_profile

urlpatterns = patterns('',

    (r'^$',
     lambda request: HttpResponseRedirect('/students/search/')),

    url(r'^search/$', search_profiles,
        name='search_profiles'),

    url(r'^display/(?P<register_number>.*)/$', display_profile,
        name='display_profile'),

)
