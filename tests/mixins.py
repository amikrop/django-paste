from django.urls import reverse

from rest_framework import status
from rest_framework.pagination import CursorPagination

from paste.views import SnippetViewSet

from tests.utils import constant, create_snippet, create_user


class SnippetTestCaseMixin:
    """Snippet test case common state and behavior."""
    constants = []

    @classmethod
    def setUpClass(cls):
        """Create and store a dummy user and a dummy staff user."""
        super().setUpClass()
        cls.user = create_user('user')
        cls.staff_user = create_user('staff', is_staff=True)

    def get(self, query_string='', **kwargs):
        """Send a GET request to the view's URL, appending given query string,
        with given kwargs, and return the response.
        """
        return self.client.get(self.url(**kwargs) + query_string)

    def assert_status(self, method_name, status_code, **kwargs):
        """Assert that a request to the view's URL with given kwargs its type
        being specified by given method name, responds with given status code.
        """
        method = getattr(self.client, method_name)
        response = method(self.url(**kwargs))
        self.assertEqual(response.status_code, status_code)

    def check_for_users(self, check, *extra_users):
        """Call given check function while representing an anonymous user, the
        dummy user, the dummy staff user and any given extra users.
        """
        for i, user in enumerate(
                (None, self.user, self.staff_user) + extra_users):
            self.client.force_authenticate(user)
            check(i)
            self.client.force_authenticate(None)

    def test_not_allowed(self):
        """This view must return a 405 Not Allowed response when accessed by
        one of its not-allowed methods.
        """
        for method in self.not_allowed:
            self.assert_status(method, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_safe_methods(self):
        """This view's safe methods must return an appropriate response
        depending on the currently authenticated user.
        """

        def check(j):
            for k, setting in enumerate(
                    [None, 'FORBID_ANONYMOUS'] + self.constants):
                with constant(setting):
                    self.assert_status(method, self.safe_expected[i][j][k])

        for i, method in enumerate(['get', 'head', 'options']):
            self.check_for_users(check)


class SnippetDetailTestCaseMixin(SnippetTestCaseMixin):
    """Snippet detail-like test case common state and behavior."""
    safe_expected = ([[
        [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN],
        [status.HTTP_200_OK] * 2, [status.HTTP_200_OK] * 2]] * 3)

    def setUp(self):
        """Create a dummy snippet."""
        create_snippet('foobaz bar', title='baz 42!')

    def url(self, pk=1):
        """Return the view's URL, for the given snippet pk."""
        return reverse(f'snippet-{self.name}', kwargs={'pk': pk})


class _SnippetPagination(CursorPagination):
    page_size = 10


class SnippetListTestCaseMixin(SnippetTestCaseMixin):
    """Snippet list-like test case common state and behavior."""
    not_allowed = ['delete', 'patch', 'put', 'trace']
    constants = ['FORBID_ANONYMOUS_LIST', 'FORBID_LIST']
    _list_expected = [
        [status.HTTP_200_OK] + [status.HTTP_403_FORBIDDEN] * 3,
        [status.HTTP_200_OK] * 3 + [status.HTTP_403_FORBIDDEN],
        [status.HTTP_200_OK] * 4]
    _options_expected = [
        [status.HTTP_200_OK] + [status.HTTP_403_FORBIDDEN]
        + [status.HTTP_200_OK] * 2,
        [status.HTTP_200_OK] * 4,
        [status.HTTP_200_OK] * 4]
    safe_expected = [_list_expected] * 2 + [_options_expected]

    def check_pagination(self, **kwargs):
        """Check that this view is able to handle pagination."""
        for i in range(20):
            create_snippet(i, **kwargs)
        SnippetViewSet.pagination_class = _SnippetPagination
        try:
            response = self.get()
            self.assertEqual(len(response.data['results']), 10)
        finally:
            SnippetViewSet.pagination_class = None
