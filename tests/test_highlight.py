from html.parser import HTMLParser

from rest_framework import status
from rest_framework.test import APITestCase

from tests.mixins import SnippetDetailTestCaseMixin
from tests.utils import constant, create_snippet


class _SnippetParser(HTMLParser):
    """Saves the text of the HTML document."""

    def __init__(self, *args, **kwargs):
        """Initialize text buffer."""
        super().__init__(*args, **kwargs)
        self.text = []

    def handle_data(self, data):
        """Add data to text buffer."""
        self.text.append(data)

    def get_text(self):
        """Return document's text."""
        return ''.join(self.text)


def _response_text(response):
    """Parse given response's HTML and return its text."""
    parser = _SnippetParser()
    parser.feed(response.data)
    return parser.get_text()


class SnippetHighlightTestCase(SnippetDetailTestCaseMixin, APITestCase):
    """Tests for the snippet highlight view."""
    name = 'highlight'
    not_allowed = ['delete', 'patch', 'post', 'put', 'trace']

    def check_response(self, response, content):
        """Check that given response has a 200 OK status code, an HTML
        content-type and given content exists in its contents.
        """
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response['Content-Type'].startswith('text/html'))
        self.assertIn(content, _response_text(response))

    def test_get_success(self):
        """Snippet highlight GET must return an HTML page of the queried
        snippet's highlighted contents.
        """
        response = self.get()
        self.check_response(response, 'foobaz bar')

    def test_title_include(self):
        """Snippet highlight GET must return a response containing the queried
        snippet's title if its embed_title is True.
        """
        response = self.get()
        self.assertIn('baz 42!', _response_text(response))

    def test_title_exclude(self):
        """Snippet highlight GET must return a response not containing the
        queried snippet's title if its embed_title is False.
        """
        snippet = create_snippet(
            'example', title='baz 43!', embed_title=False)
        response = self.get(pk=snippet.pk)
        self.assertNotIn('baz 43!', _response_text(response))

    def test_language(self):
        """Snippet highlight GET must return an HTML page of the queried
        snippet's highlighted contents if its language is set.
        """
        snippet = create_snippet('print("hello")', language='python')
        response = self.get(pk=snippet.pk)
        self.check_response(response, 'print("hello")')

    def test_default_language(self):
        """Snippet highlight GET must return an HTML page of the queried
        snippet's highlighted contents using the default language, if its
        language is not set and the GUESS_LEXER setting is False.
        """
        with constant('GUESS_LEXER', False):
            response = self.get()
        self.check_response(response, 'foobaz bar')
