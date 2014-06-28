from rest_framework import permissions


class UserUpdatePermission(permissions.BasePermission):
    """
    will be updated user matched request user
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