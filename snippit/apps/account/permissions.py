from django.shortcuts import get_object_or_404
from rest_framework import permissions
from account.models import User, Follow


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


class UserFollowPermission(permissions.BasePermission):
    """
    User Follow, UnFollow Permission
    """

    def has_permission(self, request, view):
        username = request.parser_context.get("kwargs").get("username")
        user = get_object_or_404(User, username=username)
        follow = Follow.objects.filter(following=user)
        if request.method == 'POST':
            # user himself cannot follow
            if request.user.id == user.id:
                return False
            return not follow.filter(follower=request.user).exists()
        if request.method == 'DELETE':
            # follow before for unfollow
            return follow.filter(follower=request.user).exists()
        return True