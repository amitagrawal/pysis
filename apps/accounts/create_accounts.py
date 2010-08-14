#!/usr/bin/env python

from pysis.scripts import bootstrap_django
bootstrap_django.main()

import csv
from django.db.utils import IntegrityError
from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth.models import User

from accounts.models import Profile, Course
from accounts.google_apps_manager import GoogleAppsManager


# Output of
# select distinct reg_no, name from Result where reg_no like '08MCA%' order by reg_no;
CSV_FILE = '/tmp/students.csv'
students = csv.reader(open(CSV_FILE), delimiter='|', skipinitialspace=True)

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

    first_name = first_name.strip().title()
    last_name = last_name.strip().title()

    return first_name, last_name

def is_unique(username):
    domain = settings.GOOGLE_APPS_DOMAIN
    email_id = username + '@' + domain

    exists = Profile.objects.filter(vidyalaya_email_id__iexact=email_id).exists()

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

def create_account_in_google_apps(register_number, default_passwd,
                                 first_name, last_name):

    gam = GoogleAppsManager()

    if gam.user_exists(register_number):
        print 'Google Apps account for %s already exists. Aborting' % register_number
        return

    nickname = get_new_username(first_name, last_name)

    if not nickname:
        print 'Can not get a unique Google Apps id for %s. Aborting ' % register_number
        return

    username = register_number
    password = default_passwd
    groupname = register_number[:5]

    gam.create_account(username, password,
                       first_name, last_name,
                       nickname, groupname)

    print 'Successfully Created Google Apps Account for %s' % username
    return nickname


def create_local_account(username, password,
                         first_name, last_name,
                         course_code, year_of_joining):

    course = Course.objects.get(code__iexact=course_code)

    try:
        domain = settings.GOOGLE_APPS_DOMAIN
        email = username + '@' + domain
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
    return profile

def update_profile_with_google_apps_status(register_number,
                                           nickname):
    google_apps_email_id = nickname + '@' + settings.GOOGLE_APPS_DOMAIN

    profile = Profile.objects.get(user__username__exact=register_number)

    profile.vidyalaya_email_id = google_apps_email_id
    profile.google_account_created = True
    profile.save()

def create_accounts(default_passwd):
    for register_number, name in students:
        register_number = register_number.lower()
        first_name, last_name = get_names(name)

        # First two letters of register_number represents year
        year_of_joining = register_number[:2].replace('m', '0')
        year_of_joining = int(year_of_joining) + 2000

        course_code =  register_number[2:5]

        profile = create_local_account(register_number, None,
                                       first_name, last_name,
                                       course_code, year_of_joining)

        if profile.google_account_created:
            continue

        try:
            nickname = create_account_in_google_apps(register_number, default_passwd,
                                                    first_name, last_name)
            if nickname:
                update_profile_with_google_apps_status(register_number,
                                                       nickname)
        except Exception, e:
            print 'Exception while creating Google Apps account for %s : %s' % (register_number, str(e))


if __name__ == '__main__':

    default_passwd = raw_input('Enter the default password : ')
    create_accounts(default_passwd)
