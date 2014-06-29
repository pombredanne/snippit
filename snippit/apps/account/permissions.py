from rest_framework import permissions


class UserUpdatePermission(permissions.BasePermission):
    """
    You don't have permission to update other users
    """

    def has_permission(self, request, view):
        forbidden_methods = ('PUT', 'PATCH', )
        if request.method in forbidden_methods:
            if not request.user.is_authenticated():
                return False
            # updated user
            user = view.get_object()
            # match control
            return request.user.username == user.username
        return True