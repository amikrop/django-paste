from typing import TypeVar

from django.conf import settings


T = TypeVar('T', bool, int, str)


def _setting(name: str, default: T) -> T:
    """Get value from the app's settings dict, or given default on failure."""
    try:
        settings_dict = getattr(settings, 'PASTE')
    except AttributeError:
        return default
    return settings_dict.get(name, default)


DEFAULT_EMBED_TITLE: bool = _setting('DEFAULT_EMBED_TITLE', True)

DEFAULT_LANGUAGE: str = _setting('DEFAULT_LANGUAGE', 'text')

DEFAULT_LINE_NUMBERS: bool = _setting('DEFAULT_LINE_NUMBERS', True)

DEFAULT_PRIVATE: bool = _setting('DEFAULT_PRIVATE', False)

DEFAULT_STYLE: str = _setting('DEFAULT_STYLE', 'default')

FORBID_ANONYMOUS: bool = _setting('FORBID_ANONYMOUS', False)

FORBID_ANONYMOUS_CREATE: bool = _setting('FORBID_ANONYMOUS_CREATE', False)

FORBID_ANONYMOUS_LIST: bool = _setting('FORBID_ANONYMOUS_LIST', False)

FORBID_LIST: bool = _setting('FORBID_LIST', False)

GUESS_LEXER: bool = _setting('GUESS_LEXER', True)

LIST_FOREIGN: bool = _setting('LIST_FOREIGN', True)

TITLE_MAX_LENGTH: int = _setting('TITLE_MAX_LENGTH', 100)
