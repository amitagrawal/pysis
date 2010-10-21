from django.core.urlresolvers import reverse
from admin_tools.menu import items, Menu

# to activate your custom menu add the following to your settings.py:
#
# ADMIN_TOOLS_MENU = 'django_project_template.menu.CustomMenu'

class CustomMenu(Menu):
    """
    Custom Menu for django_project_template admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children.append(items.Bookmarks(title='Bookmarks'))

        self.children.append(items.AppList(
            title='Applications',
            exclude_list=('django.contrib',)
        ))
        self.children.append(items.AppList(
            title='Administration',
            include_list=('django.contrib',)
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
