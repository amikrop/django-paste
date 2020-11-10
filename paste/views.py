from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

from paste import constants
from paste.models import Snippet
from paste.permissions import SnippetPermissions
from paste.serializers import SnippetSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """Snippet-related views.

    - Snippet list: / (GET/POST)
    - Snippet detail: /{snippet-id}/ (GET/PUT/PATCH/DELETE)
    - User snippet list: /user/{user-id}/ (GET)
    - Snippet highlight: /{snippet-id}/highlight/ (GET)
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [SnippetPermissions]

    def get_queryset(self) -> QuerySet:
        """If current user is staff return all snippets. Else, return those
        owned by current user and, if the relative setting allows so, all the
        public ones.
        """
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset

        query = Q(private=False) if constants.LIST_FOREIGN else Q(pk__in=[])
        if user.is_authenticated:
            query |= Q(owner=user)

        return queryset.filter(query)

    def perform_create(self, serializer: SnippetSerializer) -> None:
        """Store current user if authenticated, then create new instance."""
        kwargs = {}

        user = self.request.user
        if user.is_authenticated:
            kwargs['owner'] = user

        serializer.save(**kwargs)

    @action(detail=True, renderer_classes=[StaticHTMLRenderer])
    def highlight(self, request: Request, **kwargs) -> Response:
        """Highlight and return the snippet's content as HTML. If `full`
        exists as a query parameter, send a full HTML document.
        """
        instance = self.get_object()

        if instance.language:
            lexer = get_lexer_by_name(instance.language)
        elif constants.GUESS_LEXER:
            lexer = guess_lexer(instance.content)
        else:
            lexer = get_lexer_by_name(constants.DEFAULT_LANGUAGE)

        style = instance.style or constants.DEFAULT_STYLE
        options = (
            {'title': instance.title} if instance.title
            and instance.embed_title else {})
        full = 'full' in request.query_params

        formatter = HtmlFormatter(
            style=style, full=full, linenos=instance.line_numbers, **options)
        html = highlight(instance.content, lexer, formatter)
        if not full:
            css = formatter.get_style_defs()
            html = f'<style type="text/css">{css}</style>{html}'

        return Response(html)

    @action(detail=False, url_path='user/(?P<pk>[^/.]+)')
    def user(self, request: Request, pk: str, **kwargs) -> Response:
        """Return snippets belonging to user indicated by the ID in the URL.
        """
        User = get_user_model()
        owner = get_object_or_404(User, pk=pk)
        user_snippets = self.get_queryset().filter(owner=owner)

        page = self.paginate_queryset(user_snippets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(user_snippets, many=True)
        return Response(serializer.data)
