from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from core.permissions import ProfilePermission
from accounts.models import Profile, User
from accounts.serializers import AuthTokenSerializer, UserSerializer, ProfileSerializer


class CreateUserView(generics.CreateAPIView):
    """View to create a user"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """View to manage a user"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    """View to obtain an authentification token"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileView(generics.RetrieveUpdateAPIView):
    """View to see a user's profile"""
    permission_classes = (ProfilePermission,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()
