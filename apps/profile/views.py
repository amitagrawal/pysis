from datetime import date
import calendar

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.models import User

from endless_pagination.decorators import page_template

from profile.models import GeneralDetails
from profile.models import PersonalDetails
from profile.models import FamilyDetails
from profile.models import ContactDetails
from profile.models import EducationDetails
from profile.models import MiscDetails

def logoutuser(request):
  logout(request)
  return redirect('/')

@login_required
def generic_display(request, instance):
    profile, created = instance.objects.get_or_create(user=request.user)

    template = "profile/display_data.html"
    data = { 'list' : profile.as_list(),
             'user' : request.user,
             'edit' : True,
           }
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
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

    template = "profile/edit_data.html"
    data = { 'form' : form,
           }
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
@page_template("profile/search_data.html")
def display_all_students(request, 
                         template="profile/search_index.html",
                         extra_context=None):
    students_list = []

    students = User.objects.all()

    for student in students:
        name = student.first_name + ' ' + student.last_name
        register_number = student.username

        try:
            general_details =  GeneralDetails.objects.get(user=student)
            course = general_details.course
        except GeneralDetails.DoesNotExist:
            course = None

        students_list.append((name, register_number, course))

    data = { 'objects' : students_list,
           }
    if extra_context is not None:
        data.update(extra_context)
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
def display_profile(request, username):
    user = get_object_or_404(User, username=username)

    try:
       general_details =  GeneralDetails.objects.get(user=user)
       course = general_details.course
    except GeneralDetails.DoesNotExist:
        course = None

    try:
        personal_details =  PersonalDetails.objects.get(user=user)

        day = personal_details.actual_date_of_birth.day
        month = personal_details.actual_date_of_birth.month
        month_name = calendar.month_name[month]
        birth_day = '%s %s' % (day, month_name)

    except PersonalDetails.DoesNotExist:
        birth_day = None
    except AttributeError:
        birth_day = None

    try:
        contact_details =  ContactDetails.objects.get(user=user)

        personal_email_id = contact_details.personal_email_id
        vidyalaya_email_id = contact_details.vidyalaya_email_id
        personal_contact_number = contact_details.personal_contact_number

    except ContactDetails.DoesNotExist:
        personal_email_id = None
        vidyalaya_email_id = None
        personal_contact_number = None

    try:
        misc_details = MiscDetails.objects.get(user=user)
        personal_website = misc_details.personal_website

    except MiscDetails.DoesNotExist:
        personal_website = None

    profile = []

    profile.append(('Register Number', user.username))
    profile.append(('Name', user.first_name + ' ' + user.last_name))
    profile.append(('Birth Day', birth_day))
    profile.append(('Personal Email Id', personal_email_id))
    profile.append(('Vidyalaya Email Id', vidyalaya_email_id))
    profile.append(('Personal Contact Number', personal_contact_number))
    profile.append(('Personal Website', personal_website))

    template = "profile/display_data.html"
    data = { 'list' : profile,
             'user' : user,
             'edit' : False,
           }
    return render_to_response(template, data, context_instance=RequestContext(request))

