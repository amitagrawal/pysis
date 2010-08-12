from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from endless_pagination.decorators import page_template
from django.db.models import Q

from django.contrib.auth.models import User
from myprofile.models import Profile, Batch

@login_required
@page_template("students/search_data.html")
def search_profiles(request,
                    template="students/search_index.html",
                    extra_context=None):

    search_query = request.GET.get('q')

    if search_query == 'all':
        profiles = Profile.objects.all()[:100]

    else:
        profiles = Profile.objects.filter(
                       Q(user__username__icontains=search_query) |
                       Q(user__first_name__icontains=search_query) |
                       Q(user__last_name__icontains=search_query)
                   )[:100]

    context = { 'objects' : profiles,
                'title' : 'Search Results for %s' % search_query,
              }
    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def display_batch_list(request,
                       template="students/batch_list.html",
                       extra_context=None):

    batches = Batch.objects.all()

    context = {'batches' : batches}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))



@login_required
@page_template("students/search_data.html")
def display_batch(request,
                  course=None,
                  joining_year=None,
                  template="students/search_index.html",
                  extra_context=None):

    myprofile = Profile.objects.get(user=request.user)
    
    if myprofile.course and myprofile.year_of_joining:
        if course == 'myclassmates':
            course = myprofile.course.code
            joining_year = myprofile.year_of_joining
        elif course == 'myseniors':
            course = myprofile.course.code
            joining_year = myprofile.year_of_joining - 1
        elif course == 'myjuniors':
            course = myprofile.course.code
            joining_year = myprofile.year_of_joining + 1
                
    profiles = Profile.objects.all()

    if course:
        profiles = profiles.filter(course__code__iexact=course)

    if joining_year:
        profiles = profiles.filter(year_of_joining__exact=joining_year)


    if course.startswith('my'):
        title = ''
    else:
        title = 'Students of %s %s course' % (joining_year, course)        

    context = { 'objects' : profiles,
                'title' : title }
    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))



@login_required
def display_profile(request,
                    register_number,
                    template="students/display_profile.html",
                    extra_context=None):

    user = get_object_or_404(User, username=register_number)
    profile = get_object_or_404(Profile, user=user)

    context = { 'profile' : profile,
                'title' : 'Profile of %s' % profile.full_name
              }
    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))
