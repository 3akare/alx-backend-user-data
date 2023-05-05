#!/usr/bin/env python3
'''
Basic Authentication Class Module
'''
from api.v1.auth.auth import Auth
# from auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    '''
    Basic Authentication Class
    '''
    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # noqa
        '''
        extract base 64 authorization header
        '''
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        basic_values = authorization_header.split(' ')
        if basic_values[0] != 'Basic':
            return None
        else:
            return basic_values[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # noqa
        '''
        Decode extracted header with b64decode
        '''
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            byte = base64_authorization_header.encode()
            byte = b64decode(byte)
            return byte.decode()
        except Exception:
            return None

    def extract_user_credentials(self, decode_base64_authorization_header: str) -> (str, str):  # noqa
        '''
        Extract user credentials
        '''
        if decode_base64_authorization_header is None:
            return (None, None)
        if type(decode_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decode_base64_authorization_header:
            return (None, None)
        credentials = decode_base64_authorization_header.split(':', maxsplit=1)
        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # noqa
        '''
        This function should validate user credentials, but Im having issues
        importing modules and things like that, so I can't really test it
        '''
        if type(user_email) == str or type(user_pwd) == str:
            try:
                user = User.search({'email': user_email})
            except Exception:
                return None
            if len(user) <= 0:
                return None
            if user[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Basic Auth method
        '''
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        extract_header = self.extract_base64_authorization_header(auth_header)
        decode_header = self.decode_base64_authorization_header(extract_header)
        credentials = self.extract_user_credentials(decode_header)
        user = self.user_object_from_credentials(credentials[0], credentials[1])  # noqa
        return user
