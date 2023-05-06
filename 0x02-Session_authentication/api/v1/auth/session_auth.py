#!/usr/bin/env python3
'''
Session Authentication Module
'''

from api.v1.auth.auth import Auth
from models.users import User
from typing import TypeVar
# from auth import Auth
from uuid import uuid4


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
        Retrieving a link between a User ID and a Session ID
        '''
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Get current user from user_id_session and session cookie
        '''
        if request:
            session_cookie = self.session_cookie(request)
            if session_cookie:
                user_id = self.user_id_for_session_id(session_cookie)
                return User.get(user_id)
