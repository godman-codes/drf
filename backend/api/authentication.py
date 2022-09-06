from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.authtoken.models import Token


class TokenAuthentication(BaseTokenAuth):
    keyword = 'Token' # this can be edited to what ever you want it to be 

