from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from tests.mixins import SnippetListTestCaseMixin
from tests.utils import constant, create_snippet, create_user


class SnippetUserTestCase(SnippetListTestCaseMixin, APITestCase):
    """Tests for the user snippet list view."""
    not_allowed = SnippetListTestCaseMixin.not_allowed + ['post']

    def setUp(self):
        """Create and store a dummy snippet."""
        self.snippet = create_snippet('foo', owner=self.user)

    def url(self, pk=1):
        """Return the user snippet list URL, for the given user pk."""
        return reverse('snippet-user', kwargs={'pk': pk})

    def test_get_success(self):
        """User snippet list GET must return the queried user's viewable
        snippets.
        """
        snippet = create_snippet('bar', owner=self.user)
        create_snippet('baz')
        create_snippet('test', owner=self.staff_user)
        response = self.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.snippet.pk)
        self.assertEqual(response.data[1]['id'], snippet.pk)

    def test_get_private(self):
        """User snippet list GET must return private snippets only to those
        authorized to view them.
        """
        create_snippet('foo', private=True, owner=self.user)
        some_user = create_user('someuser')
        expected = [1, 2, 2, 1]

        def check(i):
            response = self.get()
            self.assertEqual(len(response.data), expected[i])

        self.check_for_users(check, some_user)

    def test_get_list_foreign(self):
        """User snippet list GET must not return snippets owned by other users
        if the LIST_FOREIGN setting is True, unless requested by a staff user.
        """
        user = create_user('someuser')
        create_snippet('test')
        expected = [0, 1, 1, 0]

        def check(i):
            response = self.get()
            self.assertEqual(len(response.data), expected[i])

        with constant('LIST_FOREIGN', False):
            self.check_for_users(check, user)

    def test_pagination(self):
        """User snippet list must be able to handle pagination."""
        self.check_pagination(owner=self.user)
