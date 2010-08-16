from hashlib import sha1
import time
import random
import socket

import gdata.apps.service
import gdata.apps.emailsettings.service
import gdata.apps.groups.service

from django.conf import settings

class GroupDoesNotExist(Exception):
    pass

class UserDoesNotExist(Exception):
    pass

class UserAlreadyExists(Exception):
    pass


class GoogleAppsManager(object):
    def __init__(self):

        self.domain = settings.GOOGLE_APPS_DOMAIN
        self.email = settings.GOOGLE_APPS_ADMIN_USERNAME
        self.password = settings.GOOGLE_APPS_ADMIN_PASSWORD

        self.apps = gdata.apps.service.AppsService(
                        domain=self.domain,
                        email=self.email,
                        password=self.password)

        self.apps.ProgrammaticLogin()
        testapps = self.apps.RetrieveUser(self.email.split('@')[0])


    def get_email_settings_object(self):
        emailsettings = gdata.apps.emailsettings.service.EmailSettingsService(domain=self.domain)
        emailsettings.SetClientLoginToken(self.apps.current_token.get_token_string())
        return emailsettings


    def get_groups_object(self):
        groups = gdata.apps.groups.service.GroupsService(domain=self.domain)
        groups.SetClientLoginToken(self.apps.current_token.get_token_string())
        return groups

    def user_exists(self, username):
        try:
            user = self.apps.RetrieveUser(username)
        except gdata.apps.service.AppsForYourDomainException, e:
            if e.reason == 'EntityDoesNotExist':
              return False
            else:
              raise e
        return True

    def create_new_user(self, username, password,
                        first_name, last_name):
        suspended = 'false'

        newhash = sha1()
        newhash.update(password)
        password = newhash.hexdigest()
        password_hash_function = 'SHA-1'

        self.apps.CreateUser(user_name=username,
                             family_name=last_name,
                             given_name=first_name,
                             password=password,
                             suspended=suspended,
                             password_hash_function=password_hash_function)


    def delete_user(self, username):
        # Rename the user to a random string, this allows the user to be recreated
        # immediately instead of waiting the usual 5 days
        timestamp = time.strftime("%Y%m%d%H%M%S")
        renameduser = username+'-'+timestamp+'-'
        randomstring = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 25))
        renameduser = renameduser+randomstring

        user = self.apps.RetrieveUser(username)
        user.login.user_name = renameduser
        self.apps.UpdateUser(username, user)

        self.apps.DeleteUser(renameduser)


    def suspend_user(self, username):
        user = self.apps.RetrieveUser(username)
        user.login.suspended = 'true'
        self.apps.UpdateUser(username, user)


    def unsuspend_user(self, username):
        user = self.apps.RetrieveUser(username)
        user.login.suspended = 'false'
        self.apps.UpdateUser(username, user)


    def create_nickname(self, username, nickname):
        self.apps.CreateNickname(username, nickname)


    def delete_nickname(self, nickname):
        self.apps.DeleteNickname(nickname)

    def delete_all_nicknames_for_user(self, username):
        for nickname in self.apps.GetGeneratorForAllNicknamesOfAUser(username):
            self.delete_nickname(nickname)

    def change_password(self, username, new_password):
        user = self.apps.RetrieveUser(username)

        newhash = sha1()
        newhash.update(new_password)
        user.login.password = newhash.hexdigest()
        user.login.hash_function_name = 'SHA-1'

        self.apps.UpdateUser(username, user)

    def group_exists(self, groupname):
        obj = self.get_groups_object()
        try:
            user = obj.RetrieveGroup(groupname)
        except gdata.apps.service.AppsForYourDomainException, e:
            if e.reason == 'EntityDoesNotExist':
              return False
            else:
              raise e
        return True

    def add_user_to_group(self, username, groupname):
        obj = self.get_groups_object()
        email = username + '@' + self.domain
        obj.AddMemberToGroup(email, groupname)


    def remove_user_from_group(self, username, groupname):
        obj = self.get_groups_object()
        email = username + '@' + self.domain
        obj.RemoveMemberFromGroup(email, groupname)

    def remove_user_from_all_groups(self, username):
        obj = self.get_groups_object()
        email_id = username + '@' + self.domain
        for groupname in obj.RetrieveGroups(email_id, direct_only=True):
            self.remove_user_from_group(username, groupname)


    def force_password_change(self, username):
        user = self.apps.RetrieveUser(username)
        user.login.change_password = 'true'
        self.apps.UpdateUser(username, user)


    def turn_off_webclips(self, username):
        obj = self.get_email_settings_object()
        obj.UpdateWebClipSettings(username=username, enable=False)


    def enable_send_as(self, username, send_as,
                       first_name, last_name,
                       make_default=True):

        full_name = first_name + ' ' + last_name
        send_as_email = send_as + '@' + self.domain
        obj = self.get_email_settings_object()

        obj.CreateSendAsAlias(username=username,
                              name=full_name,
                              address=send_as_email,
                              make_default=make_default,
                              reply_to=None)


    def create_account(self,
                       username, password,
                       first_name, last_name,
                       nickname, groupname):
        if self.user_exists(username):
            raise UserAlreadyExists, "User %s already exists" % username

        if not self.group_exists(groupname):
            raise GroupDoesNotExist, "Group %s does not exist" % groupname

        self.create_new_user(username, password,
                             first_name, last_name)

        self.force_password_change(username)
        self.turn_off_webclips(username)
        self.add_user_to_group(username, groupname)

        if nickname:
            self.create_nickname(username, nickname)
            self.enable_send_as(username, nickname,
                                first_name, last_name)

    def delete_account(self, username):
            self.remove_user_from_all_groups(username)
            self.delete_all_nicknames_for_user(username)
            self.delete_user(username)
