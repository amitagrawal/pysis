#!/usr/bin/env python

from pysis.scripts import bootstrap_django
bootstrap_django.main()

import csv
from django.db.utils import IntegrityError
from django.db import IntegrityError
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User

from accounts.models import Profile, Course
from accounts.google_apps_manager import GoogleAppsManager
from generic_app.email import send_html_mail

def get_names(full_name):
    """ Sanitizes the full_name and
        returns first_name and last_name
    """
    full_name = full_name.replace('.', ' ') # Remove Dot
    parts = full_name.split() # Remove extra whitespace and split into words

    first_name = ''
    last_name = ''
    for part in parts:
        if len(part) == 1: # Assuming that last_name has only one character
            last_name = last_name + ' ' + part
        else:
            first_name = first_name + ' ' + part

    if not last_name:
        # if there is no last name, use last part of first name
        last_name = first_name.split()[-1]
        first_name = first_name.split()[0:-1]

    if not first_name:
        # if there is no last name, use last part of first name
        first_name = last_name

    first_name = first_name.strip().title()
    last_name = last_name.strip().title()

    return first_name, last_name

def is_unique(username):
    domain = settings.GOOGLE_APPS_DOMAIN
    email_id = username + '@' + domain

    exists = Profile.objects.filter(college_email_id__iexact=email_id).exists()

    return not exists

def get_new_username(first_name,
                     last_name):
    """Returns a new, unique username for Google Apps based on the following rules:
        email_id = first word of first_name
        email_id = complete first_name without spaces
        email_id = first word of first_name + dot + first letter of last_name
        email_id = first word of first_name + dot + first word of last_name
        email_id = complete first_name without spaces + dot + first letter of last_name
        email_id = complete first_name without spaces + dot + complete last_name without spaces
        email_id = blank

    If can not find a unique email id by following these rules, return null.
    Admin has to manually set it.
    """

    first_name = first_name.lower()
    last_name = last_name.lower()
    first_word_of_first_name = first_name.split()[0]
    first_word_of_last_name = last_name.split()[0]
    first_letter_of_last_name = last_name[0]
    first_name_without_spaces = ''.join(first_name.split())
    last_name_without_spaces = ''.join(last_name.split())

    username = first_word_of_first_name
    if  is_unique(username):
        return username

    username = first_name_without_spaces
    if is_unique(username):
        return username

    username = first_word_of_first_name + '.' + first_letter_of_last_name
    if is_unique(username):
        return username

    username = first_word_of_first_name + '.' + first_word_of_last_name
    if is_unique(username):
        return username

    username = first_name_without_spaces + '.' + first_letter_of_last_name
    if is_unique(username):
        return username

    username = first_name_without_spaces + '.' + last_name_without_spaces
    if is_unique(username):
        return username


def send_introduction_mail(first_name,
                           college_email_id):

    c = {'first_name': first_name,}
    subject = "Welcome to %s" % settings.ORGANIZATION

    send_html_mail('accounts/introduction_email.html',
                   c, subject, college_email_id)


def create_account_in_google_apps(request, profile, password):

    username = profile.user.username
    first_name = profile.user.first_name
    last_name = profile.user.last_name
    college_email_id = profile.college_email_id
    nickname = college_email_id.split('@')[0]

    if profile.course.name == 'Staff':
        groupname = 'staff'
    else:
        groupname = profile.register_number[:5]

    if not college_email_id:
        messages.error(request,
             'College Email Id is empty for %s' % username)
        return

    if profile.google_account_created:
        messages.error(request,
             'College Email Id is already created for %s' % username)
        return

    try:
        gam = GoogleAppsManager()

        gam.create_account(username,
                           password,
                           first_name,
                           last_name,
                           nickname,
                           groupname
                          )

        send_introduction_mail(first_name, college_email_id)

        profile.google_account_created = True
        profile.save()

    except Exception, e:
        messages.error(request,
            'Error while creating %s. Error : %s' %
            (profile.register_number, e))
    else:
        messages.success(request,
            'Successfully created %s. Password is %s' %
            (profile.register_number, password))


def create_accounts(students):
    for register_number, name in students:
        username = register_number.lower()
        password = None
        first_name, last_name = get_names(name)
        domain = settings.GOOGLE_APPS_DOMAIN
        email = username + '@' + domain

        # First two letters of register_number represents year
        year_of_joining = register_number[:2].replace('m', '0')
        year_of_joining = int(year_of_joining) + 2000

        course_code =  register_number[2:5]
        course = Course.objects.get(code__iexact=course_code)

        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)

            user.first_name = first_name
            user.last_name = last_name
            user.save()

        except IntegrityError:
            print 'Account %s already exists' % username

        try:
            profile = Profile.objects.create(user=user,
                                             course=course,
                                             year_of_joining=year_of_joining)
        except IntegrityError:
            print 'Profile %s already exists' % username
            return

        print 'Successfully Created %s' % username


if __name__ == '__main__':
    # Output of
    # select distinct reg_no, name from Result where reg_no like '08MCA%' order by reg_no;
    CSV_FILE = '/tmp/students.csv'
    students = csv.reader(open(CSV_FILE), delimiter='|', skipinitialspace=True)
    create_accounts(students)
