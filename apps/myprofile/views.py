from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from endless_pagination.decorators import page_template

from accounts.models import Profile
from myprofile.forms import GeneralDetailsForm
from myprofile.forms import PersonalDetailsForm
from myprofile.forms import FamilyDetailsForm
from myprofile.forms import ContactDetailsForm
from myprofile.forms import EducationDetailsForm
from myprofile.forms import MiscDetailsForm


@login_required
def display_my_profile(request,
                       category='general',
                       template="myprofile/display_my_profile.html",
                       extra_context=None):
    my_profile = get_object_or_404(Profile, user=request.user)

    if category == 'general':
        data = my_profile.general_details()
    elif category == 'personal':
        data = my_profile.personal_details()
    elif category == 'family':
        data = my_profile.family_details()
    elif category == 'contact':
        data = my_profile.contact_details()
    elif category == 'education':
        data = my_profile.education_details()
    elif category == 'misc':
        data = my_profile.misc_details()
    else:
        raise Http404

    context = { 'objects' : data,
              }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def edit_my_profile(request,
                    category='general',
                    template="myprofile/edit_my_profile.html",
                    extra_context=None):
    my_profile = get_object_or_404(Profile, user=request.user)

    if category == 'general':
        model_form = GeneralDetailsForm
    elif category == 'personal':
        model_form = PersonalDetailsForm
    elif category == 'family':
        model_form = FamilyDetailsForm
    elif category == 'contact':
        model_form = ContactDetailsForm
    elif category == 'education':
        model_form = EducationDetailsForm
    elif category == 'misc':
        model_form = MiscDetailsForm
    else:
        raise Http404

    if request.method == "POST":
        form = model_form(request.POST, instance=my_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')

            redirect_path = request.path.split('edit')[0]
            return HttpResponseRedirect(redirect_path)
    else:
        form = model_form(instance=my_profile)

    context = { 'form' : form }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))

