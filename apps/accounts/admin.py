from django.contrib import admin
from django.contrib import databrowse
from django.contrib import messages
from django.conf import settings
from django.contrib.admin.util import get_deleted_objects
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.contrib.admin import helpers
from django import template

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
                    'user',
                    'college_email_id',
                    'personal_email_id',
                    'personal_contact_number',
                    'actual_date_of_birth',
                    'google_account_created',
                    'active',
                    'last_modified_on',)
    #list_editable = ('college_email_id',)

    list_filter = ('google_account_created',
                   'active',
                   'year_of_joining',
                   'course',
                   'blood_group',
                   'reservation_category',
                   )
    list_per_page = 20
    search_fields = ('user__first_name', 
                     'user__last_name',
                     'user__username',
                     'personal_email_id')
    actions = ['create_accounts_in_google',
               'delete_accounts_from_google',
               'populate_college_email_id',
               'reset_password',
               'mark_as_processed',
               'mark_as_not_processed',
               'deactivate_account',
               'reactivate_account',
              ]
    
    fieldsets = ((None, 
                  {'fields': ('user', 'course', 'year_of_joining', 'college_email_id',)
                  }
                 ),
                 ('Personal Details', 
                  {'classes': ('collapse','closed',),
                   'fields': settings.PERSONAL_DETAILS_FIELD_LIST
                  }
                 ), 
                 ('Family Details', 
                  {'classes': ('collapse','closed',),
                   'fields': settings.FAMILY_DETAILS_FIELD_LIST
                  }
                 ),                 
                 ('Contact Details', 
                  {'classes': ('collapse','closed',),
                   'fields': settings.CONTACT_DETAILS_FIELD_LIST
                  }
                 ),                 
                 ('Education Details', 
                  {'classes': ('collapse','closed',),
                   'fields': settings.EDUCATION_DETAILS_FIELD_LIST
                  }
                 ),                 
                 ('Misc Details', 
                  {'classes': ('collapse','closed',),
                   'fields': settings.MISC_DETAILS_FIELD_LIST
                  }
                 ),                 
                )
    

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

        opts = self.model._meta
        app_label = opts.app_label
    
        deletable_objects = [profile for profile in queryset] 
    
        # The user has already confirmed the deletion.
        # Do the deletion and return a None to display the change list view again.
        if request.POST.get('post'):
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
            return None
    
        context = {
            "title": "Are you sure?",
            "object_name": force_unicode(opts.verbose_name),
            "deletable_objects": [deletable_objects],
            'queryset': queryset,
            "perms_lacking": False,
            "opts": opts,
            "root_path": self.admin_site.root_path,
            "app_label": app_label,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }
    
        # Display the confirmation page
        return render_to_response('accounts/delete_from_google_apps_confirmation.html',
                                  context, 
                                  context_instance=template.RequestContext(request))        


    def populate_college_email_id(self, request, queryset):
        """Computes unique email id and populates
        """
        for profile in queryset:
            # Populate only if it is empty.
            if profile.college_email_id:
                messages.error(request,
                    'College email id is already populated for %s. Not modifying.' % profile.register_number)
            else:
                username = accounts_manager.get_new_username(profile.user.first_name,
                                                             profile.user.last_name)

                if username:
                    profile.college_email_id = username + '@' + settings.GOOGLE_APPS_DOMAIN
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
        
    def deactivate_account(self, request, queryset):
        gam = GoogleAppsManager()
        
        for profile in queryset:
            try:
                gam.suspend_user(profile.user.username)
                profile.active = False
                profile.save()
            except Exception, e:
                messages.error(request,
                    'Error while deactivating %s. Reason : %s' %
                    (profile.user.username, e))
            else:
                messages.success(request,
                    'Deactivated %s' % profile.user.username)            
        
    def reactivate_account(self, request, queryset):
        gam = GoogleAppsManager()
        
        for profile in queryset:
            try:
                gam.unsuspend_user(profile.user.username)
                profile.active = True
                profile.save()
            except Exception, e:
                messages.error(request,
                    'Error while reactivating %s. Reason : %s' %
                    (profile.user.username, e))
            else:
                messages.success(request,
                    'Reactivated %s' % profile.user.username)            


register(Course, DefaultAdmin)
register(Batch, DefaultAdmin)
register(Profile, ProfileAdmin)
