#!/usr/bin/env python3
'''
Authentication Class Module
'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''
    Authentication Class
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        require_auth: Public Method
        Return: bool
        '''
        return False

    def authorization_header(self, request=None) -> str:
        '''
        authorization_header: Public Method
        Return: None
        '''
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        current_user: Public Method
        Return: None
        '''
        return request
