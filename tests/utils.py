from contextlib import contextmanager

from django.contrib.auth import get_user_model

from paste import constants
from paste.models import Snippet


@contextmanager
def constant(name, value=True):
    """Set app constant to given value, reverting the change when cleaning up.
    """
    if name is not None:
        original = getattr(constants, name)
        setattr(constants, name, value)
    try:
        yield
    finally:
        if name is not None:
            setattr(constants, name, original)


def create_snippet(content, **kwargs):
    """Create and return a snippet, given its content and any possible kwargs.
    """
    return Snippet.objects.create(content=content, **kwargs)


def create_user(*args, **kwargs):
    """Create and return a user."""
    User = get_user_model()
    return User.objects.create_user(*args, **kwargs)
