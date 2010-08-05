from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

from profile.views import display_profile
from profile.views import display_personal_details
from profile.views import display_family_details
from profile.views import display_contact_details
from profile.views import display_education_details
from profile.views import display_misc_details

from profile.views import edit_profile
from profile.views import edit_personal_details
from profile.views import edit_family_details
from profile.views import edit_contact_details
from profile.views import edit_education_details
from profile.views import edit_misc_details

urlpatterns = patterns('',

    url(r'^$', display_profile, name='display_profile'),
    url(r'^personal/$', display_personal_details, name='display_personal_details'),
    url(r'^family/$', display_family_details, name='display_family_details'),
    url(r'^contact/$', display_contact_details, name='display_contact_details'),
    url(r'^education/$', display_education_details, name='display_education_details'),
    url(r'^misc/$', display_misc_details, name='display_misc_details'),
    
    url(r'^edit/$', edit_profile, name='edit_profile'),
    url(r'^personal/edit/$', edit_personal_details, name='edit_personal_details'),
    url(r'^family/edit/$', edit_family_details, name='edit_family_details'),
    url(r'^contact/edit/$', edit_contact_details, name='edit_contact_details'),
    url(r'^education/edit/$', edit_education_details, name='edit_education_details'),
    url(r'^misc/edit/$', edit_misc_details, name='edit_misc_details'),
    
)    