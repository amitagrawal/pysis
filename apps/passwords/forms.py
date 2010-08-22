from django import forms
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template import Context
from django.utils.http import int_to_base36
from django.contrib.sites.models import RequestSite
from django.contrib.auth.forms import SetPasswordForm

from generic_app.email import send_html_mail
from accounts.models import Profile
from accounts.google_apps_manager import GoogleAppsManager

class PasswordResetForm(forms.Form):
    register_number = forms.CharField(max_length=10)

    def clean_register_number(self):
        """
        Validates that a user exists with the given register number.
        """
        register_number = self.cleaned_data["register_number"]
        try:
            self.profile = Profile.objects.get(user__username__iexact=register_number,
                                               google_account_created__exact=True)
            self.user = self.profile.user
        except Profile.DoesNotExist:
            raise forms.ValidationError("This register number does not exist in our database.")

        if not (self.profile.personal_email_id or self.profile.personal_email_id2):
            raise forms.ValidationError("We don't have your personal email id in our records. We can not reset your password. Please contact the administrator : %s" % settings.DEFAULT_FROM_EMAIL)

        return register_number

    def save(self, 
             email_template_name='passwords/password_reset_email.html',
             request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        personal_email_id = self.profile.personal_email_id or self.profile.personal_email_id2
        request.session['personal_email_id'] = personal_email_id
        domain = RequestSite(request).domain 

        c = {
            'email': personal_email_id,
            'domain': domain,
            'uid': int_to_base36(self.user.id),
            'token': default_token_generator.make_token(self.user),
        }

        subject = "Password reset on %s" % domain
        send_html_mail(email_template_name,
                       c, 
                       subject, 
                       personal_email_id,
                       fail_silently=True)
        

class PasswordSelectForm(SetPasswordForm):
    """
    A form that lets a user change set his/her password without
    entering the old password
    """
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordSelectForm, self).__init__(user, *args, **kwargs)

    def save(self):
        username = self.user.username
        password = self.cleaned_data['new_password1']
        
        gam = GoogleAppsManager()
        gam.change_password(username, 
                            password)        
        
        return self.user
