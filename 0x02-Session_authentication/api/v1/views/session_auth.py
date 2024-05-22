#!/usr/bin/env python3
"""moduke contains a flask view that handles
all routes for the session authentication"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_session_login():
    """function that is responsible for reteiving the user based
    on the value from the email key in the request"""
    email = request.form.get('email')
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if user is None or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    user_dict = jsonify(user[0].to_json())
    user_dict.set_cookie(getenv('SESSION_NAME'), session_id)
    return user_dict


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def auth_session_logout():
    """function that logs out a user by destroying the session"""
    from api.v1.app import auth
    print('here')
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
