from django.conf.urls.defaults import *

from django.contrib import admin
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

    (r'^admin/', include(admin.site.urls)),
)
