#!/usr/bin/env python3
'''Hashing Passwords'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''
    expects one string argument name password and returns a salted
    hashed password, which is a byte string.
    '''
    hashed: bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password, password):
    """
    expects 2 arguments and returns a boolean.
    """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
