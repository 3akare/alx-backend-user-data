#!/usr/bin/env python3
'''
Session Authentication View Module
'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from os import getenv
from models.user import User


@app_views.route('/auth_session/login', method=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    '''
    POST /auth_session/login (= POST /api/v1/auth_session/login)
    '''
    email = request.form.get('email')
    if email == "" or email is None:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password == "" or password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        Auth_user = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if Auth_user is None:
        return jsonify({"error": "no user found for this email"}), 404

    if Auth_user[0].is_valid_password(password) is None:
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.auth.auth import auth
        session_id = auth.create_session(Auth_user[0].id)
        resp = jsonify(Auth_user[0].to_json())
        resp.set_cookie(getenv('SESSION_NAME'), session_id)
        return resp
