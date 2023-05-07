#!/usr/bin/env python3
'''
Session Authentication View Module
'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from os import getenv
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    '''
    POST /auth_session/login (= POST /api/v1/auth_session/login)
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            user_id = getattr(user, 'id')
            from api.v1.app import auth
            session_id = auth.create_session(user_id)
            resp = jsonify(user.to_json())
            resp.set_cookie(getenv('SESSION_NAME'), session_id)
            return resp
    return jsonify({"error": "wrong password"}), 401
