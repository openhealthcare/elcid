from opal.core.test import OpalTestCase
from elcid import Application
from opal.models import UserProfile


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
            self.menu_items_contains_url("/search/#/extract/", user)
        )

    def test_extract_superuser(self):
        self.assertTrue(
            self.menu_items_contains_url("/search/#/extract/", self.user)
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
