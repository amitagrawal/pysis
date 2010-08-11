from django.contrib import admin
from django.contrib import databrowse
import fullhistory
from fullhistory.admin import FullHistoryAdmin

from myprofile.models import Course 
from myprofile.models import Batch
from myprofile.models import Profile 

def register(model, modelAdmin):
    admin.site.register(model, modelAdmin)
    databrowse.site.register(model)
    fullhistory.register_model(model)
    
class DefaultAdmin(FullHistoryAdmin):
    pass

register(Course, DefaultAdmin)
register(Batch, DefaultAdmin)
register(Profile, DefaultAdmin)
