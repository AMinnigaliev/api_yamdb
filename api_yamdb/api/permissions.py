from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not bool(request.method in SAFE_METHODS):
            if bool(request.user and not request.user.is_anonymous):
                return bool(
                    request.user.role == 'admin' or request.user.is_superuser
                )
            return False
        return True


class IsAuthorAdminModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and (request.user.role in
                ['admin', 'moderator'] or obj.author == request.user))
        )
