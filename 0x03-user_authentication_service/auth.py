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
        Registers a user that haven't previously been registered
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

    @property
    def _generate_uuid() -> str:
        '''
        Generate UUID string
        '''
        return uuid4()


def _hash_password(password: str) -> bytes:
    '''
    expects one string argument name password and returns a salted
    hashed password, which is a byte string.
    '''
    hashed: bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed
