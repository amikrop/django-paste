from typing import List, Tuple

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from paste import constants


_lexers = (item for item in get_all_lexers() if item[1])


def _max_len(choices: List[Tuple[str, str]]) -> int:
    """Return the maximum length of the first subitems of each item."""
    return max(len(item[0]) for item in choices)


class Snippet(models.Model):
    """A source code snippet with its highlighting and privacy options. May be
    owned by a user.
    """

    LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in _lexers])
    STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

    title = models.CharField(
        _('title'), max_length=constants.TITLE_MAX_LENGTH, blank=True)
    content = models.TextField(_('content'))
    language = models.CharField(
        _('language'), choices=LANGUAGE_CHOICES,
        max_length=_max_len(LANGUAGE_CHOICES), blank=True)
    style = models.CharField(
        _('style'), choices=STYLE_CHOICES,
        max_length=_max_len(STYLE_CHOICES), blank=True)
    line_numbers = models.BooleanField(
        _('line numbers'), default=constants.DEFAULT_LINE_NUMBERS)
    embed_title = models.BooleanField(
        _('embed title'), default=constants.DEFAULT_EMBED_TITLE)
    private = models.BooleanField(
        _('private'), default=constants.DEFAULT_PRIVATE)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('last modified'), auto_now=True)
    owner = models.ForeignKey(
        get_user_model(), verbose_name=_('owner'),
        blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('snippet')
        verbose_name_plural = _('snippets')

    def __str__(self) -> str:
        return f'{self.title or _("Untitled")} ({self.pk})'
