#!/usr/bin/env python3
'''
Another Day, Another Module
'''
import bcrypt.hashpw

def _hash_password(password: str) -> bytes:
    '''
    expects one string argument name password and returns a salted
    hashed password, which is a byte string.
    '''
    hashed: bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed
