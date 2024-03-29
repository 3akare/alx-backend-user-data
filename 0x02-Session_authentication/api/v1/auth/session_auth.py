#!/usr/bin/env python3
'''
Session Authentication Module
'''

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
from uuid import uuid4
from os import getenv


class SessionAuth(Auth):
    '''
    SessionAuth Class (Inherits from auth)
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        Create Session method
        '''
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        obj = self.user_id_by_session_id
        obj[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        Retrieving a link between a User ID and a Session ID.
        '''
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        an instance method def current_user(self, request=None
        (overload) that returns a User instance based on a cookie value
        '''
        session_cookie = self.session_cookie(request)
        return User.get(self.user_id_for_session_id(session_cookie))
