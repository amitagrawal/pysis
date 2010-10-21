from django.core.urlresolvers import reverse
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

# to activate your index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_INDEX_DASHBOARD = 'django_project_template.dashboard.CustomIndexDashboard'

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for django_project_template.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        self.children.append(modules.AppList(
            title='PySIS',
            include_list=('accounts', 'django.contrib.auth'),
            css_classes=['column_1', 'collapse', 'open'],
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title='Applications',
            exclude_list=('django.contrib',),
            css_classes=['column_1', 'collapse', 'closed'],
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title='Administration',
            include_list=('django.contrib',),
            css_classes=['column_1', 'collapse', 'closed'],
        ))


        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            title='Quick links',
            css_classes=['column_2', 'collapse', 'open'],
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
            title='Recent Actions',
            css_classes=['column_2', 'collapse', 'open'],
            limit=5,
        ))


    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass


# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'django_project_template.dashboard.CustomAppIndexDashboard'

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for django_project_template.
    """
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(modules.ModelList(
            title=self.app_title,
            css_classes=['column_1', 'collapse', 'open'],
            models=self.models,
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title='Recent Actions',
            css_classes=['column_2', 'collapse', 'open'],
            include_list=self.get_app_content_types(),
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
