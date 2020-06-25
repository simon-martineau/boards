from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest

from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as DefaultAuthTokenSerializer

from accounts.models import User, Profile


class ProfileWithHyperlinkSerializer(serializers.ModelSerializer):
    """Serializer with link and name for the Profile object (READ ONLY)"""
    href = serializers.SerializerMethodField()

    def get_href(self, obj: Profile):
        """Return url for current object"""
        request = self.context['request']
        return reverse('accounts:profile', request=request, kwargs={'pk': obj.id})

    class Meta:
        model = Profile
        fields = ('href', 'username')
        read_only_fields = ('href', 'username')


# noinspection PyAbstractClass
class AuthTokenSerializer(DefaultAuthTokenSerializer):
    email = serializers.CharField(label=_("Email"))
    username = None

    def validate(self, attrs: dict) -> dict:
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
        }

    def create(self, validated_data: dict):
        """Create a new user with encrypted password and return it"""
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        """Update a user, setting the password correctly and return it"""
        if 'email' in validated_data.keys():
            validated_data.pop('email')
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile object"""
    is_self = serializers.SerializerMethodField()

    def get_is_self(self, obj: Profile) -> bool:
        """Returns if the user being serialized is the authenticated user"""
        request = self.context.get('request')  # type: HttpRequest
        if request:
            if request.user.is_authenticated:
                return obj == request.user.profile
        return False

    class Meta:
        model = Profile
        fields = ('username', 'is_self')
