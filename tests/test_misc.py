from django.utils.translation import gettext as _

from rest_framework.test import APITestCase

from paste.constants import _setting

from tests.utils import create_snippet


class SnippetModelTestCase(APITestCase):
    """Tests for the snippet model."""

    def test_str_titled(self):
        """A titled snippet's string representation must include its title and
        its pk.
        """
        snippet = create_snippet('foo', title='bar')
        self.assertEqual(str(snippet), f'bar ({snippet.pk})')

    def test_str_untitled(self):
        """An untitled snippet's string representation must include the
        localized string "Untitled" and its pk.
        """
        snippet = create_snippet('foo')
        self.assertEqual(str(snippet), f'{_("Untitled")} ({snippet.pk})')


class SettingsTestCase(APITestCase):
    """Tests for the app settings."""

    def test_no_dict(self):
        """Setting must have its requested default value if no PASTE dict is
        defined in project settings.
        """
        value = _setting('FORBID_ANONYMOUS', False)
        self.assertFalse(value)

    def test_no_key(self):
        """Setting must have its requested default value if no related key
        exists in the PASTE dict of project settings.
        """
        with self.settings(PASTE={'GUESS_LEXER': True}):
            value = _setting('FORBID_ANONYMOUS', False)
        self.assertFalse(value)

    def test_override(self):
        """Setting must have the value of the item of the project settings'
        PASTE dict with the same key.
        """
        with self.settings(PASTE={'FORBID_ANONYMOUS': True}):
            value = _setting('FORBID_ANONYMOUS', False)
        self.assertTrue(value)
