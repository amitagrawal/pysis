from django.conf.urls.defaults import *

from django.contrib import admin
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import password_change
from django.core.urlresolvers import reverse
from django.conf import settings

from misc.common_views import logoutuser, password_change_done
import myprofile

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    # This try-except is required to make nose doctest happy
    pass

urlpatterns = patterns('',
    # Example:
    # (r'^pysis/', include('pysis.foo.urls')),

    url(r'^$', 'django.contrib.auth.views.login',
        {'template_name': 'homepage/homepage.html'} ,
        name='login'),
    url(r'^logout/$', logoutuser,
        name='logout'),
    url(r'^password_change/$', 
        password_change, {'post_change_redirect' : '/password_change_done'},
        name='password_change'),
    url(r'^password_change_done/$', 
        password_change_done,
        name='password_change_done'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^browse/(.*)', login_required(databrowse.site.root)),
    (r'^announcements/', include('announcements.urls')),

    (r'^myprofile/photo/', include('avatar.urls')),
    (r'^myprofile/', include('myprofile.urls')),
    
    (r'^students/', include('students.urls')),    

    ('^attendance/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^marks/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^library/$', direct_to_template, {'template': 'coming_soon.html'}),
)
