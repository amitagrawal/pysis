from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.shortcuts import redirect
from django.views.generic import list_detail
from django.conf import settings
from django.http import HttpResponseRedirect

from students.views import search_profiles, display_batch_list, display_batch, display_profile


urlpatterns = patterns('',

    (r'^$',
     lambda request: HttpResponseRedirect(settings.STUDENTS_LANDING_URL)),
     
    url(r'^browse/$', display_batch_list,
        name='display_batch_list'),

    url(r'^browse/(?P<course>.*)/(?P<joining_year>.*)/$', display_batch,
        name='display_batch'),

    url(r'^browse/(?P<course>.*)/$', display_batch,
        name='display_batch1'),

    url(r'^search/$', search_profiles,
        name='search_profiles'),

    url(r'^display/(?P<register_number>.*)/$', display_profile,
        name='display_profile'),

)
