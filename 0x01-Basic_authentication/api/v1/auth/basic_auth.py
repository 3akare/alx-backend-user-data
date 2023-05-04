#!/usr/bin/env python3
'''
Basic Authentication Class Module
'''
try:
    # for flask
    from api.v1.auth.auth import Auth
except Exception:
    pass

try:
    # for testing the class
    from auth import Auth
except Exception:
    pass


class BasicAuth(Auth):
    '''
    Basic Authentication Class
    '''
    pass
