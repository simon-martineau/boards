from rest_framework import generics, viewsets
from rest_framework.authtoken.views import ObtainAuthToken

from core.permissions import ProfilePermission
from accounts.models import Profile
from accounts.serializers import AuthTokenSerializer, UserSerializer, ProfileSerializer


class CreateUserView(generics.CreateAPIView):
    """View to create a user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """View to obtain an authentification token"""
    serializer_class = AuthTokenSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    """View to see a user's profile"""
    permission_classes = (ProfilePermission,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()
