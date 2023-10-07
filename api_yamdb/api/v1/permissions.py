from rest_framework import permissions


class IsSuperUserOrIsAdmin(permissions.BasePermission):
    """Админ или суперюзер."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser or request.user.is_admin))


class IsAdminIsUserOrReadOnly(permissions.BasePermission):
    """Админ или авторизованный юзер или только чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)


class IsAdminIsModeratorIsAuthor(permissions.BasePermission):
    """Админ или модератор или автор."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)
