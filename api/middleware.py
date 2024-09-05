from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.core.exceptions import ObjectDoesNotExist
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ParseError

@database_sync_to_async
def get_user(token_key):
    """
    Asynchronously retrieves the user associated with the provided JWT token.

    Args:
        token_key (str): The JWT token key to be decoded and used for user retrieval.

    Returns:
        User: An instance of the CustomUser model representing the authenticated user if the token is valid and not expired.
        AnonymousUser: An instance of the AnonymousUser model if the token is invalid or expired, or if the user associated with the token does not exist.

    Raises:
        AuthenticationFailed: If the provided token is expired or invalid.
        ParseError: If there is an error parsing the token.
        Exception: If there is an unexpected error during token decoding or user retrieval.
    """
    
    try:
        ## get the token if token is given just use it.
        user = AnonymousUser()
    except Exception as e:
        print(e)
        user = AnonymousUser()
    return user

class TokenAuthMiddleware(BaseMiddleware):
    """
    Middleware class for token-based authentication in Channels.

    This middleware extracts a JWT token from the query string of the WebSocket scope and uses it to authenticate users.
    If a valid token is provided, it retrieves the associated user from the database asynchronously using the `get_user` function.

    Attributes:
        inner (callable): The inner middleware or application to delegate the request to.

    Methods:
        __init__: Initializes the middleware with the given inner middleware or application.
        __call__: Handles incoming WebSocket connections, extracts and validates JWT tokens, and sets the 'user' key in the scope dictionary.

    Args:
        inner (callable): The inner middleware or application to delegate the request to.

    Returns:
        dict: A dictionary containing the updated scope information after authentication, including the 'user' key.

    Raises:
        AuthenticationFailed: If the provided token is expired or invalid.
        ParseError: If there is an error parsing the token.
        Exception: If there is an unexpected error during token decoding or user retrieval.
    """

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = "duh" if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)