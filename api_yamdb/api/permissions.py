from rest_framework import permissions


class IsSuperUserOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser or request.user.is_staff
                     or request.user.is_admin))


class IsAdminIsUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAdminIsModeratorIsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)
