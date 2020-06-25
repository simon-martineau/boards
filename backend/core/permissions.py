from django.http import HttpRequest
from django.views import View

from rest_framework import permissions

from accounts.models import Profile
from boards.models import Topic, Post


class ProfilePermission(permissions.BasePermission):
    """Permission verifying that the user owns the profile"""

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated:
                return request.user.profile == Profile.objects.get(pk=view.kwargs['pk'])
            return False


class TopicPermission(permissions.BasePermission):
    """Permission verifying that the user owns the topic"""

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        else:
            if request.user.is_authenticated:
                return request.user.profile == Topic.objects.get(id=view.kwargs['pk']).starter or \
                    request.user.is_staff
            return False


class ReadOnlyUnlessSuperuser(permissions.BasePermission):
    """Permission verifying that only superusers can change the board"""

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_superuser
        return False


class PostPermission(permissions.BasePermission):
    """Permission that allows everyone to get, but only the owner to modify"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        else:
            if request.user.is_authenticated:
                return request.user.profile == Post.objects.get(pk=view.kwargs['pk']).author or \
                    request.user.is_staff
