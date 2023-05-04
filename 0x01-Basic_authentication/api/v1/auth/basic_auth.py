#!/usr/bin/env python3
'''
Basic Authentication Class Module
'''
from api.v1.auth.auth import Auth


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
