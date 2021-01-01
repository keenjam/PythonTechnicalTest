from rest_framework import viewsets
from rest_framework import permissions
from .models import Bond
from .serializers import BondSerializer
from rest_framework.exceptions import PermissionDenied

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
