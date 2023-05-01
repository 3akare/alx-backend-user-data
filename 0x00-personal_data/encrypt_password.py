#!/usr/bin/env python3
'''Hashing Passwords'''

import bcrypt

def hash_password(password):
    '''
     expects one string argument name password and returns a salted, hashed password, which is a byte string.
    '''
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed
