from django.conf.urls.defaults import *

from django.contrib import admin
from django.contrib import databrowse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import password_change
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static



from generic_app.views import display_homepage, logoutuser
import myprofile
import passwords

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    # This try-except is required to make nose doctest happy
    pass

urlpatterns = patterns('',
    # Example:
    # (r'^pysis/', include('pysis.foo.urls')),

    url(r'^$', display_homepage,
        name='login'),
    url(r'^logout/$', logoutuser,
        name='logout'),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
                        {'url': '%s/images/favicon.ico' % settings.STATIC_URL}),

    (r'^openid/', include('django_openid_auth.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    #(r'^browse/(.*)', login_required(databrowse.site.root)),
    #(r'^announcements/', include('announcements.urls')),

    (r'^myprofile/avatar/', include('avatar.urls')),
    (r'^myprofile/', include('myprofile.urls')),

    (r'^password/', include('passwords.urls')),

    (r'^students/', include('students.urls')),

    ('^attendance/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^marks/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^library/$', direct_to_template, {'template': 'coming_soon.html'}),
)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
