#!/usr/bin/env python3
'''
Session Authentication Module
'''

# from api.v1.auth.auth import Auth
from auth import Auth
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
