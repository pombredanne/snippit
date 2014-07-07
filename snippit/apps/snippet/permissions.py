from rest_framework import permissions


class SnippetStarPermission(permissions.BasePermission):
    """
    Snippet Star/unstar permission
    """

    def has_permission(self, request, view):
        user = request.user
        snippet = view.get_object()
        stars = user.stars.filter(snippet=snippet)
        if request.method == 'POST':
            return not stars.exists()
        elif request.method == 'DELETE':
            return stars.exists()
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