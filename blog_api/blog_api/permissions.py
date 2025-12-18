from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Allow read-only access to everyone, but only the author can edit/delete."""

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True

        author = getattr(obj, 'author', None)
        return author == request.user
