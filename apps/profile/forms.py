from django import forms

from profile.models import ProfileBase 
from profile.models import PersonalDetails
from profile.models import FamilyDetails 
from profile.models import ContactDetails 
from profile.models import EducationDetails 
from profile.models import MiscDetails 

class ProfileBaseForm(forms.ModelForm):
    class Meta:
        model = ProfileBase
        exclude = ('user')

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        exclude = ('user')

class FamilyDetailsForm(forms.ModelForm):
    class Meta:
        model = FamilyDetails
        exclude = ('user')

class ContactDetailsForm(forms.ModelForm):
    class Meta:
        model = ContactDetails
        exclude = ('user')

class EducationDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        exclude = ('user')

class MiscDetailsForm(forms.ModelForm):
    class Meta:
        model = MiscDetails
        exclude = ('user')
