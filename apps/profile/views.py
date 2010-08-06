from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings


@login_required
def generic_display(request, instance):
    profile, created = instance.objects.get_or_create(user=request.user)

    template = "profile/display_data.html"
    data = { 'list' : profile.as_list(),
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
             #'title' : description_dict[instance],
           }
    return render_to_response(template, data, context_instance=RequestContext(request))
        
