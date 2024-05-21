#!/usr/bin/env python3
"""module contains a class BasicAuth that will be used for
basic authentication"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """class BasicAuth that will be used for basic authentication"""
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """method extracts the base64 part of the Authorization header"""
        if (authorization_header is None or
                type(authorization_header) is not str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """method decodes a base64 string into a string"""
        if (base64_authorization_header is None
                or type(base64_authorization_header) is not str):
            return None
        try:
            val = base64.b64decode(base64_authorization_header).decode('utf-8')
            return val
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """method extracts user credentials from the header that
        has has been sent as an argument"""
        if (decoded_base64_authorization_header is None or
                type(decoded_base64_authorization_header) is not str or
                ':' not in decoded_base64_authorization_header):
            return (None, None)
        email: str
        passwd: str
        email, passwd = decoded_base64_authorization_header.split(':', 1)
        return (email, passwd)

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """method returns the User instance based on his email and password"""
        from models.user import User
        if (user_email is None or user_pwd is None or
                type(user_email) is not str or type(user_pwd) is not str):
            return None
        user = User()
        user_list = user.search({'email': user_email})
        if len(user_list) == 0:
            return None
        for user_obj in user_list:
            if user_obj.is_valid_password(user_pwd):
                return user_obj
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """method overloads Auth and retrieves the User
        instance for a request"""
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        email, pwd = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(email, pwd)
