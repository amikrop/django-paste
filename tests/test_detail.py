import json

from rest_framework import status
from rest_framework.test import APITestCase

from paste import constants

from tests.mixins import SnippetDetailTestCaseMixin
from tests.utils import create_snippet, create_user


class SnippetDetailTestCase(SnippetDetailTestCaseMixin, APITestCase):
    """Tests for the snippet detail view."""
    name = 'detail'
    not_allowed = ['post', 'trace']

    def request(self, method_name, **kwargs):
        """Create a dummy snippet owned by the dummy user, authenticate as the
        dummy user, then send a request to the view's URL its type being
        specified by given method name, with given kwargs, as JSON, using the
        proper content-type and return the response.
        """
        if kwargs:
            kwargs = {'data': json.dumps(kwargs)}
        snippet = create_snippet(
            'content', title='title',
            language='python', embed_title=False, owner=self.user)
        self.client.force_authenticate(self.user)
        method = getattr(self.client, method_name)
        return method(
            self.url(pk=snippet.pk),
            content_type='application/json', **kwargs)

    def test_not_found(self):
        """Snippet detail must return a 404 Not Found response when queried
        with a non-existent snippet pk.
        """
        for method in ['delete', 'get', 'head', 'patch', 'put']:
            self.assert_status(method, status.HTTP_404_NOT_FOUND, pk=2)

    def test_unsafe_methods(self):
        """Snippet detail unsafe methods must return an appropriate response
        depending on the currently authenticated user.
        """
        owner = create_user('owner')
        expected = [
            [status.HTTP_403_FORBIDDEN] * 2
            + [status.HTTP_204_NO_CONTENT] * 2,
            [status.HTTP_403_FORBIDDEN] * 2 + [status.HTTP_200_OK] * 2,
            [status.HTTP_403_FORBIDDEN] * 2
            + [status.HTTP_400_BAD_REQUEST] * 2]

        def check(j):
            snippet = create_snippet('baz', owner=owner)
            self.assert_status(method, expected[i][j], pk=snippet.pk)
            snippet.delete()

        for i, method in enumerate(['delete', 'patch', 'put']):
            self.check_for_users(check, owner)

    def test_get_success(self):
        """Snippet detail GET must return the queried snippet."""
        response = self.request('get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'content')
        self.assertEqual(response.data['title'], 'title')
        self.assertEqual(response.data['language'], 'python')
        self.assertEqual(response.data['style'], '')
        self.assertEqual(
            response.data['line_numbers'], constants.DEFAULT_LINE_NUMBERS)
        self.assertFalse(response.data['embed_title'])
        self.assertEqual(response.data['private'], constants.DEFAULT_PRIVATE)
        self.assertEqual(response.data['owner'], self.user.pk)

    def test_get_private(self):
        """Snippet detail GET must return the private queried snippet only to
        those authorized to view it.
        """
        owner = create_user('owner')
        snippet = create_snippet('testing', private=True, owner=owner)
        expected = [status.HTTP_404_NOT_FOUND] * 2 + [status.HTTP_200_OK] * 2

        def check(i):
            self.assert_status('get', expected[i], pk=snippet.pk)

        self.check_for_users(check, owner)

    def test_patch_success(self):
        """Snippet detail PATCH must partially update the queried snippet."""
        response = self.request('patch', title='foobar', line_numbers=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'content')
        self.assertEqual(response.data['title'], 'foobar')
        self.assertEqual(response.data['language'], 'python')
        self.assertEqual(response.data['style'], '')
        self.assertFalse(response.data['line_numbers'])
        self.assertFalse(response.data['embed_title'])
        self.assertEqual(response.data['private'], constants.DEFAULT_PRIVATE)
        self.assertEqual(response.data['owner'], self.user.pk)

    def test_put_success(self):
        """Snippet detail PUT must update the queried snippet."""
        response = self.request('put', content='test', private=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'test')
        self.assertEqual(response.data['title'], 'title')
        self.assertEqual(response.data['language'], 'python')
        self.assertEqual(response.data['style'], '')
        self.assertEqual(
            response.data['line_numbers'], constants.DEFAULT_LINE_NUMBERS)
        self.assertFalse(response.data['embed_title'])
        self.assertTrue(response.data['private'])
        self.assertEqual(response.data['owner'], self.user.pk)

    def test_put_no_content(self):
        """Snippet detail PUT must return a 400 Bad Request response if no
        content field is set.
        """
        response = self.request('put', style='friendly')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
