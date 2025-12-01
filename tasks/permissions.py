from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to allow only owners of an object or staff users to edit/delete it.
    Read-only requests are allowed for any request (adjust if you want different behavior).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return getattr(obj, 'owner', None) == request.user or request.user and request.user.is_staff
