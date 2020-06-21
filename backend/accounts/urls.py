from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts import views


app_name = 'accounts'
urlpatterns = [
    path('auth/create', views.CreateUserView.as_view(), name='create'),
    path('auth/token', views.CreateTokenView.as_view(), name='token'),
    path('users/profiles/<slug:pk>', views.ProfileView.as_view(), name='profile')
]
