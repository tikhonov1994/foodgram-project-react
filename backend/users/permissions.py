from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class GetPost(IsAuthenticated):
    def has_permission(self, request, view):
        request.method in SAFE_METHODS or request.method == 'POST'
        return True


class CurrentUserOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user== obj.author