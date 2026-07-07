from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.models import AnonymousUser

import jwt
import os

from dotenv import load_dotenv

load_dotenv()

ENCODING_SECRET = os.getenv("ENCODING_SECRET")


class MerchantIntegration(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        
        scheme,_,token = auth_header.partition(" ")
        if scheme.lower() != "bearer":
            raise AuthenticationFailed("Expected Bearer apikey in header")
        payload = self.validate_apikey(token)

        return (AnonymousUser(),payload)


    def validate_apikey(self,apikey):
        try:
            payload = jwt.decode(apikey,ENCODING_SECRET,algorithms=["HS256"])
            return payload
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid ApiKey")
