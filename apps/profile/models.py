from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    )

RESERVATION_CATEGORY_CHOICES = (
    ('OC', 'OC'),
    ('OBC', 'OBC'),
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


class Course(models.Model):
    course_name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.course_name


class GeneralDetails(models.Model):
    user = models.ForeignKey(User, unique=True)

    course = models.ForeignKey(Course, null=True, blank=True)
    year_of_joining = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'General Details'
        verbose_name_plural = 'GeneralDetails'
        
    def __unicode__(self):
        #return '%s - %s' % (self.user.username, self.user.first_name)
        return self.user.username
    
    def as_list(self):
        result = []

        result.append(('Name', self.user.first_name + ' ' + self.user.last_name))        
        result.append(('Register Number', self.user.username))
        result.append(('Course', self.course))
        result.append(('Year of Joining', self.year_of_joining))
        
        return result

class PersonalDetails(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    gender = models.CharField(max_length=2,
                              choices=GENDER_CHOICES,
                              default='M')
    blood_group = models.CharField(max_length=4, choices=BLOOD_GROUP_CHOICES,null=True, blank=True)
    date_of_birth = models.DateField(help_text="What is your date of birth as per records?",null=True, blank=True)
    actual_date_of_birth = models.DateField(help_text="When do you celebrate your birthday?",null=True, blank=True)

    class Meta:
        verbose_name = 'Personal Details'
        verbose_name_plural = 'Personal Details'
        
    def __unicode__(self):
        #return '%s - %s' % (self.user.username, self.user.first_name)
        return self.user.username
    
    def as_list(self):
        result = []
        
        result.append(('Gender', self.gender))
        result.append(('Blood Group', self.blood_group))
        result.append(('Date of Birth', self.date_of_birth))
        result.append(('Actual Date of Birth', self.actual_date_of_birth))
        
        return result


class FamilyDetails(models.Model):
    user = models.ForeignKey(User, unique=True)
    
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

    class Meta:
        verbose_name = 'Family Details'
        verbose_name_plural = 'Family Details'
        
    def __unicode__(self):
        #return '%s - %s' % (self.user.username, self.user.first_name)
        return self.user.username
        
    def as_list(self):
        result = []
        
        result.append(("Father's Name", self.father_name))
        result.append(("Father's Profession", self.father_profession))
        result.append(('Family Income', self.family_income))
        result.append(('Religion', self.religion))
        result.append(('Caste', self.caste))
        result.append(('Reservation Category', self.reservation_category))
        
        return result
    
    
class ContactDetails(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    personal_email_id = models.EmailField(max_length=75, null=True, blank=True)
    vidyalaya_email_id = models.EmailField(max_length=75, null=True, blank=True)
    personal_contact_number = models.IntegerField(null=True, blank=True)
    emergency_contact_number = models.IntegerField(null=True, blank=True)
    present_address = models.TextField(null=True, blank=True)
    permanent_address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Contact Details'
        verbose_name_plural = 'Contact Details'
        
    def __unicode__(self):
        #return '%s - %s' % (self.user.username, self.user.first_name)
        return self.user.username

    def as_list(self):
        result = []
        
        result.append(('Personal Email Id', self.personal_email_id))
        result.append(('Vidyalaya Email Id', self.vidyalaya_email_id))
        result.append(('Personal Contact Number', self.personal_contact_number))
        result.append(('Emergency Contact Number', self.emergency_contact_number))
        result.append(('Present Address', self.present_address))
        result.append(('Permanent Address', self.permanent_address))
        
        return result



class EducationDetails(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    sslc_passed_out_year = models.IntegerField(null=True, blank=True)
    sslc_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    hslc_passed_out_year = models.IntegerField(null=True, blank=True)
    hslc_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hslc_major = models.CharField(max_length=30, null=True, blank=True)

    ug_passed_out_year = models.IntegerField(null=True, blank=True)
    ug_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    ug_major = models.CharField(max_length=30, null=True, blank=True)

    pg_passed_out_year = models.IntegerField(null=True, blank=True)
    pg_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    pg_major = models.CharField(max_length=30, null=True, blank=True)

    #history_of_arrears = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Education Details'
        verbose_name_plural = 'Education Details'
        
    def __unicode__(self):
        #return '%s - %s' % (self.user.username, self.user.first_name)
        return self.user.username    
    
    def as_list(self):
        result = []
        
        result.append(('SSLC Passed-out Year', self.sslc_passed_out_year))
        result.append(('SSLC Percentage', self.sslc_percentage))

        result.append(('HSLC Passed-out Year', self.hslc_passed_out_year))
        result.append(('HSLC Percentage', self.hslc_percentage))
        result.append(('HSLC Major', self.hslc_major))
        
        result.append(('UG Passed-out Year', self.ug_passed_out_year))
        result.append(('UG Percentage', self.ug_percentage))
        result.append(('UG Major', self.ug_major))
        
        result.append(('PG Passed-out Year', self.pg_passed_out_year))
        result.append(('PG Percentage', self.pg_percentage))
        result.append(('PG Major', self.pg_major))
        
        return result    


class MiscDetails(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    nss = models.BooleanField(blank=True)
    ncc = models.BooleanField(blank=True)
    sports = models.CharField(max_length=100, null=True, blank=True)
    hobbies = models.CharField(max_length=100, null=True, blank=True)
    personal_website = models.URLField(null=True, blank=True, verify_exists=False)

    class Meta:
        verbose_name = 'Extra Curricular Activities'
        verbose_name_plural = 'Extra Curricular Activities'
        
    def __unicode__(self):
        #return '%s - %s' % (self.user.username, self.user.first_name)
        return self.user.username    

    def as_list(self):
        result = []
        
        result.append(('NSS', self.nss))
        result.append(('NCC', self.ncc))
        result.append(('Sports', self.sports))
        result.append(('Hobbies', self.hobbies))
        result.append(('Personal Website', self.personal_website))
        
        return result    

