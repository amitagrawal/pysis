from django.conf.urls.defaults import *

from django.contrib import admin
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template


import profile

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    # This try-except is required to make nose doctest happy
    pass

urlpatterns = patterns('',
    # Example:
    # (r'^pysis/', include('pysis.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^profile/', include('profile.urls')),
    (r'^profile/photo/', include('avatar.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^browse/(.*)', login_required(databrowse.site.root)),
    (r'^announcements/', include('announcements.urls')),
    
    url(r'^accounts/$', 'django.contrib.auth.views.login',
        {'template_name': 'account/login.html'} ,
        name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
        name='logout'),
        
    ('^attendance/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^marks/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^library/$', direct_to_template, {'template': 'coming_soon.html'}),
)
