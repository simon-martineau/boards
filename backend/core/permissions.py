from django.http import HttpRequest
from django.views import View
from django.shortcuts import get_object_or_404

from rest_framework import permissions

from accounts.models import Profile


class ProfilePermission(permissions.BasePermission):
    """Permission verifying that the user owns the profile"""

    def has_permission(self, request: HttpRequest, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated:
                return request.user.profile == get_object_or_404(Profile, pk=view.kwargs.get('pk'))
            return False


class ReadOnlyUnlessSuperuser(permissions.BasePermission):
    """Permission verifying that only superusers can change the board"""

    def has_permission(self, request: HttpRequest, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_superuser
        return False
