from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token # this is to generate auth tokens after registering it as on of the apps in the settings.py
from .views import api_home
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('', api_home, name='api_home'),
    path('auth/', obtain_auth_token, name='auth_token'), # this is a method call to the auth token view that generates the auth token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]