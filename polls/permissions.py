# polls/permissions.py
from rest_framework.permissions import BasePermission


class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view) -> bool:
        return  request.user.is_authenticated


class IsStaffUser(BasePermission):
    def has_permission(self, request, view) -> bool:
        return  request.user.is_staff
