from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

from profile.models import ProfileBase 
from profile.models import PersonalDetails
from profile.models import FamilyDetails 
from profile.models import ContactDetails 
from profile.models import EducationDetails 
from profile.models import MiscDetails

from profile.forms import ProfileBaseForm 
from profile.forms import PersonalDetailsForm
from profile.forms import FamilyDetailsForm
from profile.forms import ContactDetailsForm 
from profile.forms import EducationDetailsForm 
from profile.forms import MiscDetailsForm  

description_dict = {
    ProfileBase : 'Basic Details',
    PersonalDetails : 'Personal Details',
    FamilyDetails : 'Family Details',
    ContactDetails : 'Contact Details',
    EducationDetails : 'Education Details',
    MiscDetails : 'Misc Details',
}

def generic_view(request, instance):
    profile, created = instance.objects.get_or_create(user=request.user)

    template = "profile/display_form.html"
    data = { 'list' : profile.as_list(),
             'title' : description_dict[instance],
             'settings' : settings,
           }
    return render_to_response(template, data, context_instance=RequestContext(request))
    

@login_required
def display_profile(request):
    return generic_view(request, ProfileBase)

@login_required
def display_personal_details(request):
    return generic_view(request, PersonalDetails)

@login_required
def display_family_details(request):
    return generic_view(request, FamilyDetails)

@login_required
def display_contact_details(request):
    return generic_view(request, ContactDetails)

@login_required
def display_education_details(request):
    return generic_view(request, EducationDetails)

@login_required
def display_misc_details(request):
    return generic_view(request, MiscDetails)


def generic_edit(request, instance, instance_form):
    profile, created = instance.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = instance_form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')

            redirect_path = request.path.split('edit')[0]
            return HttpResponseRedirect(redirect_path)
    else:
        form = instance_form(instance=profile)

    template = "profile/edit_form.html"
    data = { 'form' : form,
             'title' : description_dict[instance],
             'settings' : settings,
           }
    return render_to_response(template, data, context_instance=RequestContext(request))
    


def edit_profile(request):
    return generic_edit(request, ProfileBase, ProfileBaseForm)

@login_required
def edit_personal_details(request):
    return generic_edit(request, PersonalDetails, PersonalDetailsForm)

@login_required
def edit_family_details(request):
    return generic_edit(request, FamilyDetails, FamilyDetailsForm)

@login_required
def edit_contact_details(request):
    return generic_edit(request, ContactDetails, ContactDetailsForm)

@login_required
def edit_education_details(request):
    return generic_edit(request, EducationDetails, EducationDetailsForm)

@login_required
def edit_misc_details(request):
    return generic_edit(request, MiscDetails, MiscDetailsForm)
    
