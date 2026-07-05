from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied



class IsActuallyLoggedIn(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            raise PermissionDenied("You are not currently logged in.")

        return True

class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type != "system_admin":
            raise PermissionDenied("This request is only available to system administrators.")

        return True


class IsMerchantAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type != "merchant_admin":
            raise PermissionDenied("This request is only available to Merchant administrators")

        return True

class IsAnAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type not in ["system_admin","merchant_admin"]:
            raise PermissionDenied("This request is only available to administrators.")

        return True

class IsACustomer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type != "customer":
            raise PermissionDenied("This request is available to only customers.")

        return True
