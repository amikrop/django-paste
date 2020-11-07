from html.parser import HTMLParser

from rest_framework import status
from rest_framework.test import APITestCase

from tests.mixins import SnippetDetailTestCaseMixin
from tests.utils import constant, create_snippet


class _SnippetParser(HTMLParser):
    """Saves the text of the HTML tree and decides whether it is dealing with
    a full HTML document.
    """

    def __init__(self, *args, **kwargs):
        """Initialize text buffer and `full` flag."""
        super().__init__(*args, **kwargs)
        self.text = []
        self.full = False

    def handle_data(self, data):
        """Add data to text buffer."""
        self.text.append(data)

    def handle_starttag(self, tag, attrs):
        """If found tag is <html>, set the `full` flag to True."""
        if tag == 'html':
            self.full = True

    def get_text(self):
        """Return document's text."""
        return ''.join(self.text)


def _response_text(response):
    """Parse given response's HTML and return its text."""
    parser = _SnippetParser()
    parser.feed(response.data)
    return parser.get_text()


def _is_full(response):
    """Parse given response's HTML and decide whether it is a full HTML
    document.
    """
    parser = _SnippetParser()
    parser.feed(response.data)
    return parser.full


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
        snippet's title if its embed_title field is True and `full` exists as
        a query parameter.
        """
        response = self.get('?full')
        self.assertIn('baz 42!', _response_text(response))

    def test_title_exclude(self):
        """Snippet highlight GET must return a response not containing the
        queried snippet's title if its embed_title field is False.
        """
        snippet = create_snippet(
            'example', title='baz 43!', embed_title=False)
        response = self.get('?full', pk=snippet.pk)
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

    def test_not_full(self):
        """Snippet highlight GET must not return a full HTML document if
        `full` does not exist as a query parameter.
        """
        for query_string in ['', '?', '?ful', '?foo=1']:
            response = self.get(query_string)
            self.assertFalse(_is_full(response))

    def test_full(self):
        """Snippet highlight GET must return a full HTML document if
        `full` exists as a query parameter.
        """
        for query_part in ['', '=', '=0', '=1' '=a', '=foo', '=k&full=test']:
            response = self.get(f'?full{query_part}')
            self.assertTrue(_is_full(response))
