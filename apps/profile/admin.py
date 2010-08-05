from django.contrib import admin
from django.contrib import databrowse
import fullhistory
from fullhistory.admin import FullHistoryAdmin

from profile.models import Course 
from profile.models import ProfileBase 
from profile.models import PersonalDetails 
from profile.models import FamilyDetails 
from profile.models import ContactDetails 
from profile.models import EducationDetails 
from profile.models import MiscDetails 

def register(model, modelAdmin):
    admin.site.register(model, modelAdmin)
    databrowse.site.register(model)
    fullhistory.register_model(model)
    
class DefaultAdmin(FullHistoryAdmin):
    pass

register(Course, DefaultAdmin)
register(ProfileBase, DefaultAdmin)
register(PersonalDetails, DefaultAdmin)
register(FamilyDetails, DefaultAdmin)
register(ContactDetails, DefaultAdmin)
register(EducationDetails, DefaultAdmin)
register(MiscDetails, DefaultAdmin)

