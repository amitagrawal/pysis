#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated, changes may be lost if you
# go and generate it again. It was generated with the following command:
# ./manage.py dumpscript accounts auth.user

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.utils import IntegrityError

def run():
    from accounts.models import Course

    accounts_course_1 = Course()
    accounts_course_1.code = u'MCA'
    accounts_course_1.name = u'MCA'
    accounts_course_1.duration = 3L
    accounts_course_1.level = u'PG'
    try:
        accounts_course_1.save()
    except IntegrityError:
        pass

    from accounts.models import Batch

    accounts_batch_1 = Batch()
    accounts_batch_1.code = u'09mca'
    accounts_batch_1.course = accounts_course_1
    accounts_batch_1.year = 2009L
    accounts_batch_1.name = u'MCA 2009-2012 Batch'
    try:
        accounts_batch_1.save()
    except IntegrityError:
        pass


    from django.contrib.auth.models import User

    auth_user_2 = User()
    auth_user_2.username = settings.TEST_USERNAME
    auth_user_2.first_name = u'Test'
    auth_user_2.last_name = u'User'
    auth_user_2.email = u''
    auth_user_2.is_staff = False
    auth_user_2.is_active = True
    auth_user_2.is_superuser = False
    try:
        auth_user_2.save()
    except IntegrityError:
        pass

    auth_user_2 = User.objects.get(username=settings.TEST_USERNAME)
    auth_user_2.set_password(settings.TEST_USER_PASSWORD)
    auth_user_2.save()


    from accounts.models import Profile

    accounts_profile_1 = Profile()
    accounts_profile_1.user = auth_user_2
    accounts_profile_1.course = accounts_course_1
    accounts_profile_1.year_of_joining = Decimal('2009')
    accounts_profile_1.college_email_id = u'test@rmv.ac.in'
    accounts_profile_1.gender = u'M'
    accounts_profile_1.actual_date_of_birth = datetime.date(2009, 6, 1)
    try:
        accounts_profile_1.save()
    except IntegrityError:
        pass
