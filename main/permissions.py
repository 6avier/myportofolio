"""Role checks for the portfolio.

Roles:
- owner:  a superuser, can create, update and delete.
- editor: a member of the "Editor" Django Group (assigned via /admin), can update only.
- everyone else: read only (registered users can also star).
"""

EDITOR_GROUP = "Editor"


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP).exists()


def can_edit(user):
    return user.is_superuser or is_editor(user)
