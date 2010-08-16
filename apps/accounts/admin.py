from django.contrib import admin
from django.contrib import databrowse
from django.contrib import messages
from django.conf import settings
import fullhistory
from fullhistory.admin import FullHistoryAdmin

from django.contrib.auth.models import User
from accounts.models import Course, Batch, Profile
from accounts.google_apps_manager import GoogleAppsManager
from accounts import accounts_manager

def register(model, modelAdmin):
    admin.site.register(model, modelAdmin)
    databrowse.site.register(model)
    fullhistory.register_model(model)

class DefaultAdmin(FullHistoryAdmin):
    pass

class ProfileAdmin(FullHistoryAdmin):

    # Options for admin
    list_display = ('full_name',
                    'register_number',
                    'vidyalaya_email_id',
                    'personal_email_id',
                    'google_account_created',
                    'last_modified_on',)
    #list_editable = ('vidyalaya_email_id',)

    list_filter = ('google_account_created',
                   'year_of_joining',
                   'course',)
    list_per_page = 20
    search_fields = ('user__first_name', 
                     'user__last_name',
                     'user__username',
                     'personal_email_id')
    actions = ['create_accounts_in_google',
               'delete_accounts_from_google',
               'populate_vidyalaya_email_id',
               'reset_password',
               'mark_as_processed',
               'mark_as_not_processed',
              ]

    def create_accounts_in_google(self, request, queryset):
        """Creates the Google Apps account for the user
        """
        gam = GoogleAppsManager()
        password = User.objects.make_random_password(length=6)

        for profile in queryset:
            accounts_manager.create_account_in_google_apps(request, profile, password)


    def delete_accounts_from_google(self, request, queryset):
        """Deletes the user from Google Apps database
        """

        for profile in queryset:
            try:
                gam = GoogleAppsManager()
                gam.delete_account(profile.user.username)
            except Exception, e:
                messages.error(request,
                    'Error while deleting %s. Error : %s' %
                    (profile.register_number, e))
            else:
                messages.success(request,
                    'Successfully deleted %s' % profile.register_number)

    def populate_vidyalaya_email_id(self, request, queryset):
        """Computes unique email id and populates
        """
        for profile in queryset:
            # Populate only if it is empty.
            if profile.vidyalaya_email_id:
                messages.error(request,
                    'Vidyalaya email id is already populated for %s. Not modifying.' % profile.register_number)
            else:
                username = accounts_manager.get_new_username(profile.user.first_name,
                                                             profile.user.last_name)

                if username:
                    profile.vidyalaya_email_id = username + '@' + settings.GOOGLE_APPS_DOMAIN
                    profile.save()
                else:
                    messages.error(request,
                        'Could not generate a unique username for %s' % profile.register_number)


    def reset_password(self, request, queryset):
        gam = GoogleAppsManager()
        passwd = User.objects.make_random_password(length=6)

        for profile in queryset:
            if not profile.google_account_created:
                messages.error(request,
                    'No Google Apps account for %s' % profile.register_number)
                continue

            try:
                username = profile.register_number
                result = gam.change_password(username,
                                             passwd)
            except Exception, e:
                messages.error(request,
                    'Failed to update password for %s. Reason : %s' %
                    (username, e))
            else:
                messages.success(request,
                    'Successfully updated password for %s. New Password is %s' %
                    (username, passwd))

    def mark_as_processed(self, request, queryset):
        queryset.update(google_account_created=True)

    def mark_as_not_processed(self, request, queryset):
        queryset.update(google_account_created=False)


register(Course, DefaultAdmin)
register(Batch, DefaultAdmin)
register(Profile, ProfileAdmin)
