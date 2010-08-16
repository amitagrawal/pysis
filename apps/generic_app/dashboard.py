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
        self.columns = 3
        Dashboard.__init__(self, **kwargs)

        self.children.append(modules.AppList(
            title='PySIS',
            include_list=('accounts', 'django.contrib.auth'),
            css_classes=['collapse', 'open'],
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title='Administration',
            include_list=('django.contrib',),
            css_classes=['collapse', 'closed'],
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title='Applications',
            exclude_list=('django.contrib',),
            css_classes=['collapse', 'closed'],
        ))

        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            title='Quick links',
            column=3,
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=True,
            children=[
                {
                    'title': 'Return to site',
                    'url': '/',
                },
                {
                    'title': 'Change password',
                    'url': reverse('admin:password_change'),
                },
                {
                    'title': 'Log out',
                    'url': reverse('admin:logout')
                },
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            column=3,
            title='Recent Actions',
            limit=5,
            css_classes=['collapse', 'closed'],
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
