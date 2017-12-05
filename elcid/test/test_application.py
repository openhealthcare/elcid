from opal.core.test import OpalTestCase
from elcid import Application
from opal.models import UserProfile
from microhaem.constants import MICROHAEM_ROLE
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser


class ApplicationMenuItemsTestCase(OpalTestCase):
    def menu_items_contains_url(self, url, user):
        return any(
            i for i in Application.get_menu_items(user=user) if i.href == url
        )

    def test_extract_permission(self):
        user = self.make_user('blah')
        UserProfile.objects.create(
            user=user,
            can_extract=True
        )
        self.assertFalse(user.is_superuser)
        self.assertTrue(
            self.menu_items_contains_url("/#/extract/", user)
        )

    def test_extract_superuser(self):
        self.assertTrue(
            self.menu_items_contains_url("/#/extract/", self.user)
        )

    def test_extract_neither(self):
        user = self.make_user('blah')
        UserProfile.objects.create(
            user=user,
            can_extract=False
        )
        self.assertFalse(user.is_superuser)
        self.assertFalse(
            self.menu_items_contains_url("/#/extract/", user)
        )

    def test_profile_microhaem(self):
        user = self.make_user('blah')
        profile = UserProfile.objects.create(
            user=user,
        )
        profile.roles.create(name=MICROHAEM_ROLE)
        self.assertTrue(
            self.menu_items_contains_url("/pathway/#/haem_referral", user)
        )

    def test_profile_not_microhaem(self):
        user = self.make_user('blah')
        UserProfile.objects.create(
            user=user,
        )
        self.assertFalse(
            self.menu_items_contains_url("/pathway/#/haem_referral", user)
        )

    def test_logged_out_user_gets_login_menuitem(self):
        user = AnonymousUser()
        self.assertTrue(
            self.menu_items_contains_url(reverse("login"), user)
        )

    def test_logged_out_user_does_not_get_any_other_menuitems(self):
        user = AnonymousUser()
        self.assertEqual(len(Application.get_menu_items(user=user)), 1)
