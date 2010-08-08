from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from endless_pagination.decorators import page_template
from django.db.models import Q

from django.contrib.auth.models import User
from myprofile.models import Profile

@login_required
@page_template("students/search_data.html")
def search_profiles(request, 
                    template="students/search_index.html",
                    extra_context=None):
    
    search_query = request.GET.get('q')
    
    if search_query == 'all' or search_query is None:
        profiles = Profile.objects.all()[:100]

    elif search_query == 'myclassmates':
        batch = request.user.username[:5]
        profiles = Profile.objects.filter(user__username__startswith=batch)

    elif search_query == 'myseniors':
        batch = int(request.user.username[:2])-1
        batch = '%02d' % batch + request.user.username[2:5]
        profiles = Profile.objects.filter(user__username__startswith=batch)

    elif search_query == 'myjuniors':
        batch = int(request.user.username[:2])+1
        batch = '%02d' % batch + request.user.username[2:5]
        profiles = Profile.objects.filter(user__username__startswith=batch)
        
    else:
        profiles = Profile.objects.filter(
                       Q(user__username__icontains=search_query) |
                       Q(user__first_name__icontains=search_query) |
                       Q(user__last_name__icontains=search_query)
                   )[:100]

    context = { 'objects' : profiles,
                'search_query' : search_query,
              }
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
              }
    if extra_context is not None:
        context.update(extra_context)
        
    return render_to_response(template, context, context_instance=RequestContext(request))
