import datetime, calendar

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from managers import ProfileManager

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    )

RESERVATION_CATEGORY_CHOICES = (
    ('OC', 'OC'),
    ('OBC', 'OBC'),
    ('MBC', 'MBC'),
    ('BC', 'BC'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    )

BLOOD_GROUP_CHOICES = (
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    )

COURSE_LEVELS = (
    ('UG', 'Under Graduate'),
    ('PG', 'Post Graduate'),
    )

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50, unique=True)
    duration = models.IntegerField(help_text='Duration of the course in years')
    level = models.CharField(max_length=4,
                             choices=COURSE_LEVELS,
                             default='UG')

    objects = models.Manager()

    def __unicode__(self):
        return self.name

class Batch(models.Model):
    code = models.CharField(max_length=5, unique=True,
                            help_text='First 5 characters of register number')
    course = models.ForeignKey(Course, null=True, blank=True)
    year = models.IntegerField()
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["course", "-year"]
        verbose_name_plural = "Batches"


class Profile(models.Model):
    # Register Number, First Name and Last Name are defined in User model
    user = models.ForeignKey(User, unique=True,)

    objects = ProfileManager()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    @property
    def register_number(self):
        return self.user.username

    @property
    def last_login(self):
        return self.user.last_login

    @property
    def birth_day(self):
        if self.actual_date_of_birth:
            day = self.actual_date_of_birth.day
            month = calendar.month_name[self.actual_date_of_birth.month]
            return '%s %s' % (month, day)

    # GeneralDetails
    course = models.ForeignKey(Course, null=True, blank=True)
    year_of_joining = models.DecimalField(max_digits=4, decimal_places=0, null=True, blank=True)
    college_email_id = models.EmailField(max_length=75, null=True, blank=True)


    # PersonalDetails
    gender = models.CharField(max_length=2,
                              choices=GENDER_CHOICES,
                              default='M')
    blood_group = models.CharField(max_length=4, choices=BLOOD_GROUP_CHOICES,null=True, blank=True)
    date_of_birth = models.DateField(help_text='What is your date of birth as per records?',null=True, blank=True)
    actual_date_of_birth = models.DateField(help_text='When do you celebrate your birthday?',null=True, blank=True)


    # FamilyDetails
    father_name = models.CharField(max_length=100, null=True, blank=True)
    father_profession = models.CharField(max_length=100, null=True, blank=True)
    family_income = models.IntegerField(null=True, blank=True)
    religion = models.CharField(max_length=30,
                             null=True, blank=True)
    caste = models.CharField(max_length=30,
                             null=True, blank=True)
    reservation_category = models.CharField(max_length=10,
                                            choices=RESERVATION_CATEGORY_CHOICES,
                                            null=True, blank=True)


    # Contact Details
    personal_email_id = models.EmailField(max_length=75, null=True, blank=True)
    personal_email_id2 = models.EmailField(max_length=75, null=True, blank=True)
    personal_contact_number = models.CharField(max_length=20, null=True, blank=True)
    personal_contact_number2 = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)
    present_address = models.TextField(null=True, blank=True)
    permanent_address = models.TextField(null=True, blank=True)


    # EducationDetails
    sslc_passed_out_year = models.DecimalField(max_digits=4, decimal_places=0, null=True, blank=True)
    sslc_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    hslc_passed_out_year = models.DecimalField(max_digits=4, decimal_places=0, null=True, blank=True)
    hslc_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hslc_major = models.CharField(max_length=30, null=True, blank=True)

    ug_passed_out_year = models.DecimalField(max_digits=4, decimal_places=0, null=True, blank=True)
    ug_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                        help_text='Percentage till now')
    ug_major = models.CharField(max_length=30, null=True, blank=True)

    pg_passed_out_year = models.DecimalField(max_digits=4, decimal_places=0, null=True, blank=True)
    pg_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                        help_text='Percentage till now')
    pg_major = models.CharField(max_length=30, null=True, blank=True)

    history_of_arrears = models.TextField(null=True, blank=True)


    # Misc Details
    nss = models.BooleanField(blank=True)
    ncc = models.BooleanField(blank=True)
    sports = models.CharField(max_length=100, null=True, blank=True)
    hobbies = models.CharField(max_length=100, null=True, blank=True)
    personal_website = models.URLField(null=True, blank=True, verify_exists=False)
    orkut_profile_url = models.URLField(null=True, blank=True, verify_exists=False)
    facebook_profile_url = models.URLField(null=True, blank=True, verify_exists=False)
    linkedin_profile_url = models.URLField(null=True, blank=True, verify_exists=False)

    # Audit Trail
    active = models.BooleanField(default=True)
    google_account_created = models.BooleanField(default=False)
    last_modified_on = models.DateTimeField(editable=False,
                                            auto_now=True)

    def __unicode__(self):
        return '%s %s - %s' % (self.user.first_name, self.user.last_name, self.user.username )
        #return self.user.username

    def slice(self, fields_list):
        slice = []

        for field in fields_list:
            slice.append((field.replace('_', ' '), self.__getattribute__(field)))

        return slice

    def general_details(self):
        return self.slice(settings.GENERAL_DETAILS_FIELD_LIST)

    def personal_details(self):
        return self.slice(settings.PERSONAL_DETAILS_FIELD_LIST)

    def family_details(self):
        return self.slice(settings.FAMILY_DETAILS_FIELD_LIST)

    def contact_details(self):
        return self.slice(settings.CONTACT_DETAILS_FIELD_LIST)

    def education_details(self):
        return self.slice(settings.EDUCATION_DETAILS_FIELD_LIST)

    def misc_details(self):
        return self.slice(settings.MISC_DETAILS_FIELD_LIST)

    def search_preview(self):
        return self.slice(settings.PROFILE_PREVIEW_FIELD_LIST)

    def search_fullview(self):
        return self.slice(settings.PROFILE_FULLVIEW_FIELD_LIST)

    class Meta:
        ordering = ['-last_modified_on']
