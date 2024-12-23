from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Разрешение для менеджера магазина.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

class IsClient(permissions.BasePermission):
    """
    Разрешение для клиента.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client