#!/usr/bin/env python

import pysis.scripts.bootstrap_django

import csv
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from myprofile.models import Profile, Course

# Meaning p
PASSWD = 'sha1$eac2a$36d970cfe5781f78c04e6b15ef7a4dc661d7eb71'

# Output of
# select distinct reg_no, name from Result where reg_no like '08MCA%' order by reg_no;
CSV_FILE = '/tmp/students.csv'
students = csv.reader(open(CSV_FILE), delimiter='|', skipinitialspace=True)

def create_default_courses():
    course_list = [
        ['MCA', 'MCA', 3, 'PG'],
        ['BCA', 'BCA', 3, 'UG'],
        ['BSB', 'BSc Computer Science', 3, 'UG'],
        ['BIT', 'BSc IT', 3, 'UG'],
        ['BCM', 'BCom', 3, 'UG'],
        ]
    
    for code, name, duration, level in course_list:
        try:
            c = Course(code=code, name=name, duration=duration, level=level)
            c.save()
            print 'Created %s' % name
        except IntegrityError:
            print '%s already exists' % name
        
     
def get_names(name):
    name = name.replace('.', ' ') # Remove Dot
    parts = name.split() # Remove extra whitespace and split into words

    first_name = ''
    last_name = ''
    for part in parts:
        if len(part) == 1:
            last_name = last_name + ' ' + part
        else:
            first_name = first_name + ' ' + part

    first_name = first_name.strip().title()
    last_name = last_name.strip().title()

    return first_name, last_name

def create_users():
    for register_number, name in students:
        register_number = register_number.lower()
        first_name, last_name = get_names(name)
        
        # First two letters of register_number represents year 
        year_of_joining = register_number[:2].replace('m', '0')
        year_of_joining = int(year_of_joining) + 2000
        
        course_code =  register_number[2:5]
        course = Course.objects.get(code__iexact=course_code)
    
        try:
            user = User(username=register_number, 
                        password=PASSWD, 
                        first_name=first_name, 
                        last_name=last_name)
            user.save()
    
            profile = Profile(user=user, 
                              course=course,
                              year_of_joining=year_of_joining)
            profile.save()
    
            print 'Created %s' % register_number
    
        except Exception as e:
            print 'Error while creating %s : %s' % (register_number, str(e))
            

if __name__ == '__main__':
    create_default_courses()
    create_users()
