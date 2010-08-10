
from pysis.settings.settings import *

INSTALLED_APPS = list(INSTALLED_APPS)
# django-sane-testing is throwing errors when south is enabled. So disable south
INSTALLED_APPS.remove('south')


URLS_TO_TEST = [
    '/',
    #'/admin',
    #'/browse',
    '/myprofile',
    '/students',
    #'/attendance',
    #'/library',
    #'/marks',
    
    '/myprofile/general',
    '/myprofile/personal',
    '/myprofile/family',
    '/myprofile/contact',
    '/myprofile/education',
    '/myprofile/misc',
    '/myprofile/general/edit',
    '/myprofile/personal/edit',
    '/myprofile/family/edit',
    '/myprofile/contact/edit',
    '/myprofile/education/edit',
    '/myprofile/misc/edit',
    
    '/myprofile/photo/change',
    '/myprofile/photo/delete',
    
    '/students/search/?q=all',
    '/students/search/?q=myclassmates',
    '/students/search/?q=myjuniors',
    '/students/search/?q=myseniors',
    '/students/search/?q=somejunk',
    
    '/students/display/09mca001',
    
    '/password_change',
                
]

PUBLIC_URLS = [
    '/',               
]

# Test urls ending with / also
URLS_TO_TEST += [url + '/' for url in URLS_TO_TEST]
PUBLIC_URLS  += [url + '/' for url in PUBLIC_URLS]
