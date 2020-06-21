from django.urls import path

from accounts import views


app_name = 'accounts'
urlpatterns = [
    path('auth/create', views.CreateUserView.as_view(), name='create'),
    path('auth/token', views.CreateTokenView.as_view(), name='token'),
]
