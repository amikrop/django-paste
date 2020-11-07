from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from paste import constants
from paste.models import Snippet


class SnippetPermissions(permissions.BasePermission):
    """Permissions for snippet-related views."""

    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Decide regarding current user type and settings for anonymous
        access, listing, anonymous listing and anonymous creation.
        """
        user = request.user
        if constants.FORBID_ANONYMOUS and user.is_anonymous:
            return False

        if view.action in ['list', 'user']:
            if constants.FORBID_LIST:
                return user.is_staff  # type: ignore
            if constants.FORBID_ANONYMOUS_LIST:
                return user.is_authenticated

        return not (
            view.action == 'create'
            and constants.FORBID_ANONYMOUS_CREATE and user.is_anonymous)

    def has_object_permission(
            self, request: Request, view: ViewSet, obj: Snippet) -> bool:
        """Allow if method is safe and snippet is public, or if user is owner
        or staff.
        """
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS  # type: ignore
            and not obj.private or obj.owner == user or user.is_staff)
