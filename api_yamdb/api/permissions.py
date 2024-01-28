from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )


class IsAuthorAdminModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and obj.author
            and (
                obj.author == request.user
                or request.user.role in ['admin', 'moderator']
            )
        )
