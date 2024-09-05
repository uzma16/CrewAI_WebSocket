from datetime import datetime, timedelta

import jwt
from django.conf import settings
from Profile.models import CustomUser
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

User = CustomUser()
class JWTAuthentication(authentication.BaseAuthentication):
    """
    Provides JWT-based authentication for Django REST Framework.

    This authentication class decodes and verifies JWT tokens extracted from the Authorization header of HTTP requests.
    It also provides methods for creating JWT tokens and extracting tokens from headers.

    Attributes:
        User (CustomUser): The model class representing the authenticated user.

    Methods:
        authenticate: Authenticates the user based on the JWT token extracted from the request header.
        authenticate_header: Returns the authentication scheme to be included in the WWW-Authenticate header.
        create_jwt: Creates a new JWT token for the specified user.
        get_the_token_from_header: Extracts the token from the Authorization header and cleans it.

    Args:
        authentication.BaseAuthentication: The base authentication class provided by Django REST Framework.

    Returns:
        tuple: A tuple containing the authenticated user and the token payload extracted from the JWT token.

    Raises:
        AuthenticationFailed: If the JWT signature is invalid or if the user is not found based on the token payload.
        ParseError: If there is an error parsing the token or decoding the JWT.
    """

    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)  # clean the token

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        # Get the user from the database
        username_or_phone_number = payload.get('user_identifier')
        if username_or_phone_number is None:
            raise AuthenticationFailed('User identifier not found in JWT')
        
        user = User.nodes.filter(username=username_or_phone_number).first()
        if user is None:
            user = User.nodes.filter(phone_number=username_or_phone_number).first()
            if user is None:
                raise AuthenticationFailed('User not found')

        # Return the user and token payload
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user):
        """
        Creates a new JWT access token for the specified user.

        Args:
            user (CustomUser): The user for whom the token is created.

        Returns:
            str: The JWT access token.
        """
        # Create the JWT payload
        payload = {
            'user_identifier': user.username,
            'exp': int((datetime.now() + timedelta(seconds=settings.JWT_CONF['ACCESS_TOKEN_LIFETIME'])).timestamp()),
            # set the expiration time for 5 hour from now
            'iat': datetime.now().timestamp(),
            'username': user.username,
        }

        # Encode the JWT with your secret key
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token
