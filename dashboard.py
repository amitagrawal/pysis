from django.core.urlresolvers import reverse
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

# to activate your index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_INDEX_DASHBOARD = 'pysis.dashboard.CustomIndexDashboard'

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for pysis.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # append a link list module for "quick links"
        #self.children.append(modules.LinkList(
        #    title=_('Quick links'),
        #    layout='inline',
        #    draggable=False,
        #    deletable=False,
        #    collapsible=False,
        #    children=[
        #        {
        #            'title': _('Return to site'),
        #            'url': '/',
        #        },
        #        {
        #            'title': _('Change password'),
        #            'url': reverse('admin:password_change'),
        #        },
        #        {
        #            'title': _('Log out'),
        #            'url': reverse('admin:logout')
        #        },
        #    ]
        #))
        
        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title='Administration',
            include_list=('django.contrib',),
            css_classes=['collapse', 'open'],
        ))
        
        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title='Applications',
            exclude_list=('django.contrib',),
            css_classes=['collapse', 'open'],
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            column=2,
            title='Recent Actions',
            limit=5
        ))

        # append a feed module
        self.children.append(modules.Feed(
            column=2,
            title='Latest Django News',
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            column=2,
            title='Support',
            children=[
                {
                    'title': 'Django documentation',
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': 'Django "django-users" mailing list',
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': 'Django irc channel',
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass


# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'pysis.dashboard.CustomAppIndexDashboard'

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for pysis.
    """
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(modules.ModelList(
            title=self.app_title,
            models=self.models,
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            column=2,
            title='Recent Actions',
            include_list=self.get_app_content_types(),
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
