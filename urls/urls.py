from django.conf.urls.defaults import *

from django.contrib import admin
from django.contrib import databrowse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import password_change
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import redirect

from generic_app.views import logoutuser
import myprofile

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    # This try-except is required to make nose doctest happy
    pass

@login_required
def password_change_done(request):
    messages.success(request, 'Successfully changed your password.')
    return redirect(settings.MY_PROFILE_LANDING_URL)

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

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
                        {'url': '%s/images/favicon.ico' % settings.MEDIA_URL}),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^browse/(.*)', login_required(databrowse.site.root)),
    #(r'^announcements/', include('announcements.urls')),

    (r'^myprofile/photo/', include('avatar.urls')),
    (r'^myprofile/', include('myprofile.urls')),

    (r'^students/', include('students.urls')),

    ('^attendance/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^marks/$', direct_to_template, {'template': 'coming_soon.html'}),
    ('^library/$', direct_to_template, {'template': 'coming_soon.html'}),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
