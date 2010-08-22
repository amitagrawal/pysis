from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from passwords.forms import PasswordResetForm

@csrf_protect
def password_reset(request,
                   template_name='passwords/password_reset_form.html',
                   email_template_name='passwords/password_reset_email.html',
                   post_reset_redirect=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {}
            opts['email_template_name'] = email_template_name
            opts['request'] = request
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = PasswordResetForm()

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))
