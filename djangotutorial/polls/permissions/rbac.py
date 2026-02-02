# polls/permissions/rbac.py
from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    required_roles: set[str] = set()

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False

        user_roles = set(
            request.user.groups.values_list("name", flat=True)
        )
        return bool(user_roles & self.required_roles)
