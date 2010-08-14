from django.conf import settings
from django import forms

from accounts.models import Profile


class GeneralDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = list(set(settings.GENERAL_DETAILS_FIELD_LIST) - set(['first_name', 'last_name', 'register_number']))

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = settings.PERSONAL_DETAILS_FIELD_LIST

class FamilyDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = settings.FAMILY_DETAILS_FIELD_LIST

class ContactDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = settings.CONTACT_DETAILS_FIELD_LIST

class EducationDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = settings.EDUCATION_DETAILS_FIELD_LIST

class MiscDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =settings. MISC_DETAILS_FIELD_LIST

