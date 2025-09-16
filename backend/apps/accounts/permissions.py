from rest_framework.permissions import BasePermission


class IsStaffRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in ('preparateur', 'caissier', 'admin') or user.is_staff
