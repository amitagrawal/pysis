from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def logoutuser(request):
  logout(request)
  return redirect('/')

