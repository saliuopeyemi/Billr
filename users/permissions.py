from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied



class IsActuallyLoggedIn(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            raise PermissionDenied("You are not currently logged in.")

        return True
