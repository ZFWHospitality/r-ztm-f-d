from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Admins (is_staff) can edit/delete anything; else only owner
        return request.user.is_staff or obj.owner == request.user
