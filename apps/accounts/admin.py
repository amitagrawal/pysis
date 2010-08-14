from django.contrib import admin
from django.contrib import databrowse
import fullhistory
from fullhistory.admin import FullHistoryAdmin

from accounts.models import Course
from accounts.models import Batch
from accounts.models import Profile

def register(model, modelAdmin):
    admin.site.register(model, modelAdmin)
    databrowse.site.register(model)
    fullhistory.register_model(model)

class DefaultAdmin(FullHistoryAdmin):
    pass

#class ProfileAdmin(FullHistoryAdmin):

    ## Options for admin
    #list_display = ('first_name',
                    #'last_name',
                    #'register_number',
                    #'vidyalaya_email_id',
                    #'processed',
                    #'last_modified_on',)
    ##list_editable = ('vidyalaya_email_id',)
    #list_filter = ('processed',)
    #list_per_page = 20
    #search_fields = ('first_name', 'last_name', 'register_number',)
    #actions = ['create_accounts_in_google',
               #'delete_accounts_from_google',
               #'populate_vidyalaya_email_id',
               #'reset_password',
               #'mark_as_processed',
               #'mark_as_not_processed',
              #]

    #def create_accounts_in_google(self, request, queryset):
        #"""Creates the user in Google Apps database
        #"""
        #for registration in queryset:
            #result = gam_actions.create(registration)

            #if result:
                #self.message_user(request,
                                  #'Failed to create "%s" for %s. Reason = %s' %
                                      #(registration.vidyalaya_email_id,
                                       #registration.register_number,
                                       #result))
            #else:
                #self.message_user(request, "Successfully created %s" % registration.vidyalaya_email_id)
                #registration.processed = True
                #registration.save()

    #def delete_accounts_from_google(self, request, queryset):
        #"""Deletes the user from Google Apps database
        #"""
        #for registration in queryset:
            #result = gam_actions.delete(registration)

            #if result:
                #self.message_user(request,
                                  #'Failed to delete %s. Reason = %s' %
                                  #(registration.vidyalaya_email_id, result))
            #else:
                #self.message_user(request, "Successfully deleted %s" % registration.vidyalaya_email_id)
                #registration.processed = False
                #registration.save()


    #def populate_vidyalaya_email_id(self, request, queryset):
        #"""Computes unique email id and populates
        #"""
        #for registration in queryset:
            ## Populate only if it is empty.
            #if registration.vidyalaya_email_id:
                #logging.info("Vidyalaya email id is already populated for %s. Not modifying." % registration.register_number)
            #else:
                #email_id = vidyalaya_policy.get_new_email_id(
                                            #registration.first_name,
                                            #registration.last_name,
                                            #registration.register_number)
                #logging.debug("Generated %s for %s" % (email_id, registration.register_number))

                #if email_id:
                    #registration.vidyalaya_email_id = email_id
                    #registration.save()
                #else:
                    #self.message_user(request, "Could not generate a unique email id. Human wisdom is required")

        #self.message_user(request, "Completed")

    #def reset_password(self, request, queryset):
        #for registration in queryset:
            #result = gam_actions.reset(registration)

            #if result:
                #self.message_user(request, "Failed to reset password for %s" % registration.vidyalaya_email_id)
            #else:
                #self.message_user(request, "Successfully reset password for %s" % registration.vidyalaya_email_id)

    #def mark_as_processed(self, request, queryset):
        #queryset.update(processed=True)

    #def mark_as_not_processed(self, request, queryset):
        #queryset.update(processed=False)


register(Course, DefaultAdmin)
register(Batch, DefaultAdmin)
register(Profile, DefaultAdmin)
