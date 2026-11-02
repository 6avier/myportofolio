"""Role checks for the portfolio.

Roles:
- owner:  a superuser, can create, update and delete.
- editor: a member of the "Editor" Django Group (assigned via /admin), can update only.
- everyone else: read only (registered users can also star).
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS

EDITOR_GROUP = "Editor"


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP).exists()


def can_edit(user):
    return user.is_superuser or is_editor(user)


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.method in ("PUT", "PATCH") and is_editor(request.user)
