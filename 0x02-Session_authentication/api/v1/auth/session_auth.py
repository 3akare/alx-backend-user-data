#!/usr/bin/env python3
'''
Session Authentication Module
'''

from auth import Auth
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

    def session_cookie(self, request=None):
        '''
        Accessing request cookies :)
        '''
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
