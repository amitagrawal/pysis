from django.conf.urls.defaults import *

from django.contrib import admin
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

from profile.views import logoutuser
import profile

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

    (r'^profile/photo/', include('avatar.urls')),
    (r'^profile/', include('profile.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^browse/(.*)', login_required(databrowse.site.root)),
    (r'^announcements/', include('announcements.urls')),

    ('^attendance/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^marks/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^library/$', direct_to_template, {'template': 'coming_soon.html'}),
)
