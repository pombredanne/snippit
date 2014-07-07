from rest_framework import permissions


class SnippetStarPermission(permissions.BasePermission):
    """
    Snippet Star/unstar permission
    """

    def has_permission(self, request, view):
        user = request.user
        if request.method == 'POST':
            snippet = view.get_object()
            return not user.stars.filter(snippet=snippet).exists()
        elif request.method == 'DELETE':
            snippet = view.get_object()
            return user.stars.filter(snippet=snippet).exists()
        return True


class SnippetDestroyUpdatePermission(permissions.BasePermission):
    """
    Snippet Destroy Update Permission
    """

    def has_permission(self, request, view):
        user = request.user
        forbidden_methods = ('PUT', 'PATCH', 'DELETE')
        if request.method in forbidden_methods:
            snippet = view.get_object()
            return snippet.created_by.username == user.username
        return True