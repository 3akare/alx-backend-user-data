#!/usr/bin/env python3
'''
Another Day, Another Module
'''
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user that hasn't been registered
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email=email, hashed_password=_hash_password(password))  # noqa
            return user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate users login
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if user:
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)  # noqa
        return False

    def create_session(self, email: str) -> str:
        """
        Create Session ID for users
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            session_id = None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        '''
        Get User from session id
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> User:
        '''
        Destroy session by user id
        '''
        try:
            self._db.update_user(user_id=user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        '''
        Reset password token
        '''
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        Update password
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)  # noqa


def _hash_password(password: str) -> bytes:
    '''
    expects one string argument name password and returns a salted
    hashed password, which is a byte string.
    '''
    hashed: bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    '''
    Generate UUID string
    '''
    return str(uuid4())
