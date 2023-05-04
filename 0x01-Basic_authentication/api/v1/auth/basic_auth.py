#!/usr/bin/env python3
'''
Basic Authentication Class Module
'''
try:
    from api.v1.auth.auth import Auth
except Exception:
    pass

try:
    from auth import Auth
except Exception:
    pass


class BasicAuth(Auth):
    '''
    Basic Authentication Class
    '''
    pass
