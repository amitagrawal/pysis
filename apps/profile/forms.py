from django import forms

from profile.models import GeneralDetails 
from profile.models import PersonalDetails
from profile.models import FamilyDetails 
from profile.models import ContactDetails 
from profile.models import EducationDetails 
from profile.models import MiscDetails 

class GeneralDetailsForm(forms.ModelForm):
    class Meta:
        model = GeneralDetails
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
