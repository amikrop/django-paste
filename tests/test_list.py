import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from paste import constants

from tests.mixins import SnippetListTestCaseMixin
from tests.utils import constant, create_snippet, create_user


class SnippetListTestCase(SnippetListTestCaseMixin, APITestCase):
    """Tests for the snippet list view."""

    def url(self):
        """Return the snippet list URL."""
        return reverse('snippet-list')

    def post(self, **kwargs):
        """Send a POST request to the view's URL with data indicated by given
        kwargs, as JSON, using the proper content-type, and return the
        response.
        """
        return self.client.post(
            self.url(), data=json.dumps(kwargs),
            content_type='application/json')

    def test_get_success(self):
        """Snippet list GET must return all the viewable snippets."""
        create_snippet('foo')
        create_snippet('bar')
        response = self.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['content'], 'foo')
        self.assertEqual(response.data[1]['content'], 'bar')

    def test_get_private(self):
        """Snippet list GET must return private snippets only to those
        authorized to view them.
        """
        owner = create_user('owner')
        create_snippet('foo', private=True, owner=owner)
        expected = [0, 0, 1, 1]

        def check(i):
            response = self.get()
            self.assertEqual(len(response.data), expected[i])

        self.check_for_users(check, owner)

    def test_get_list_foreign(self):
        """Snippet list GET must not return snippets owned by other users if
        the LIST_FOREIGN setting is True, unless requested by a staff user.
        """
        create_snippet('foo')
        create_snippet('bar', owner=self.user)
        expected = [0, 1, 2]

        def check(i):
            response = self.get()
            self.assertEqual(len(response.data), expected[i])

        with constant('LIST_FOREIGN', False):
            self.check_for_users(check)

    def test_post_success(self):
        """Snippet list POST must create a new snippet."""
        response = self.post(
            content='foo', style='friendly', embed_title=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'foo')
        self.assertEqual(response.data['title'], '')
        self.assertEqual(response.data['language'], '')
        self.assertEqual(response.data['style'], 'friendly')
        self.assertEqual(
            response.data['line_numbers'], constants.DEFAULT_LINE_NUMBERS)
        self.assertFalse(response.data['embed_title'])
        self.assertEqual(response.data['private'], constants.DEFAULT_PRIVATE)
        self.assertIsNone(response.data['owner'])

    def test_post_owner(self):
        """Snippet list POST must store currently authenticated user as the
        newly created snippet's owner.
        """
        self.client.force_authenticate(self.user)
        response = self.post(content='foo')
        self.assertEqual(response.data['owner'], self.user.pk)

    def test_post_no_content(self):
        """Snippet list POST must return a 400 Bad Request response if no
        content field is set.
        """
        response = self.post(title='foo')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_oversized_title(self):
        """Snippet list POST must return a 400 Bad Request response if the
        title field consists of more characters than the TITLE_MAX_LENGTH
        setting indicates.
        """
        title = 'a' * (constants.TITLE_MAX_LENGTH + 1)
        response = self.post(content='foo', title=title)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_invalid(self):
        """Snippet list POST must return a 400 Bad Request response if a value
        different than the available choices is set for a multiple choice
        field.
        """
        for field in ['language', 'style']:
            response = self.post(
                **{'content': 'foo', field: '123-invalid-abc'})
            self.assertEqual(
                response.status_code, status.HTTP_400_BAD_REQUEST)

    def check_post_forbid_anonymous(self, setting):
        """Check that snippet list POST returns a 403 Forbidden response to
        anonymous users if the given setting is True.
        """
        expected = (
            [status.HTTP_403_FORBIDDEN] + [status.HTTP_400_BAD_REQUEST] * 2)

        def check(i):
            response = self.post()
            self.assertEqual(response.status_code, expected[i])

        with constant(setting):
            self.check_for_users(check)

    def test_post_forbid_anonymous(self):
        """Snippet list POST must return a 403 Forbidden response to anonymous
        users if the FORBID_ANONYMOUS setting is True.
        """
        self.check_post_forbid_anonymous('FORBID_ANONYMOUS')

    def test_post_forbid_anonymous_create(self):
        """Snippet list POST must return a 403 Forbidden response to anonymous
        users if the FORBID_ANONYMOUS_CREATE setting is True.
        """
        self.check_post_forbid_anonymous('FORBID_ANONYMOUS_CREATE')

    def test_post_anonymous_private(self):
        """Snippet list POST must return a 400 Bad Request response to
        anonymous users who attempt to create a private snippet.
        """
        response = self.post(content='foo', private=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pagination(self):
        """Snippet list must be able to handle pagination."""
        self.check_pagination()
