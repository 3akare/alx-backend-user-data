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
        if (path is None or excluded_paths is None or excluded_paths == []):
            return True

        for paths in excluded_paths:
            if path in paths or path + '/' in paths:
                return False
        return True

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
