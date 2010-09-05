from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def display_homepage(request,
                     template="homepage/homepage.html",
                     extra_context=None):
    if request.user.is_authenticated():
        return redirect(settings.HOMEPAGE_FOR_LOGGEDIN_USERS)
    else:
        return render_to_response(template, extra_context, context_instance=RequestContext(request))
        

    

@login_required
def logoutuser(request):
  logout(request)
  return redirect(settings.LOGOUT_REDIRECT_URL)

