from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token # this is to generate auth tokens after registering it as on of the apps in the settings.py
from .views import api_home

urlpatterns = [
    path('', api_home, name='api_home'),
    path('auth/', obtain_auth_token, name='auth_token'), # this is a method call to the auth token view that generates the auth token
]