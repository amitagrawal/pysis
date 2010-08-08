from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

def logoutuser(request):
  logout(request)
  return redirect('/')

@login_required  
def password_change_done(request):
    messages.success(request, 'Successfully changed your password.')
    return redirect(settings.MY_PROFILE_LANDING_URL)