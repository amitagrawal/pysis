from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

from profile.views import generic_display
from profile.views import generic_edit

from profile.models import GeneralDetails 
from profile.models import PersonalDetails
from profile.models import FamilyDetails 
from profile.models import ContactDetails 
from profile.models import EducationDetails 
from profile.models import MiscDetails

from profile.forms import GeneralDetailsForm 
from profile.forms import PersonalDetailsForm
from profile.forms import FamilyDetailsForm
from profile.forms import ContactDetailsForm 
from profile.forms import EducationDetailsForm 
from profile.forms import MiscDetailsForm  


urlpatterns = patterns('',

    url(r'^general/$', 
        generic_display, {'instance':GeneralDetails},
        name='display_general_details'),
    url(r'^personal/$', 
        generic_display, {'instance':PersonalDetails},
        name='display_personal_details'),
    url(r'^family/$', 
        generic_display, {'instance':FamilyDetails},
        name='display_family_details'),
    url(r'^contact/$', 
        generic_display, {'instance':ContactDetails},
        name='display_contact_details'),
    url(r'^education/$', 
        generic_display, {'instance':EducationDetails},
        name='display_education_details'),
    url(r'^misc/$', 
        generic_display, {'instance':MiscDetails},
        name='display_misc_details'),
    
    url(r'^general/edit/$', 
        generic_edit, {'instance':GeneralDetails, 'instance_form':GeneralDetailsForm},
        name='edit_general_details'),
    url(r'^personal/edit/$', 
        generic_edit, {'instance':PersonalDetails, 'instance_form':PersonalDetailsForm},
        name='edit_personal_details'),
    url(r'^family/edit/$', 
        generic_edit, {'instance':FamilyDetails, 'instance_form':FamilyDetailsForm},
        name='edit_family_details'),
    url(r'^contact/edit/$', 
        generic_edit, {'instance':ContactDetails, 'instance_form':ContactDetailsForm},
        name='edit_contact_details'),
    url(r'^education/edit/$', 
        generic_edit, {'instance':EducationDetails, 'instance_form':EducationDetailsForm},
        name='edit_education_details'),
    url(r'^misc/edit/$', 
        generic_edit, {'instance':MiscDetails, 'instance_form':MiscDetailsForm},
        name='edit_misc_details'),
    
)    