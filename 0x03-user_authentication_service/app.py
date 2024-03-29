#!/usr/bin/env python3
'''
Flask Application
'''

from auth import Auth
from flask import jsonify, Flask, request, abort, redirect

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    '''
    index Function
    '''
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    '''
    Register users
    '''
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''
    Login Users in and save their cookies
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    '''
    Destroys a user's session and redirect the user to the index page
    '''
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    '''
    Profile function
    '''
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_token() -> str:
    '''
    get token
    '''
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        if token is None:
            abort(403)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    '''
    Update password
    '''
    email, token, password = request.form.get('email'), request.form.get('reset_token'), request.form.get('new_password')  # noqa
    try:
        AUTH.update_password(token, password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
