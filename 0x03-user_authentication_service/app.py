#!/usr/bin/env python3
"""this module contains code for a simple flask app
that has one url"""
from flask import Flask, json, jsonify, request, abort, redirect
from sqlalchemy.orm import session, strategy_options
from auth import Auth


app: Flask = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'],
           strict_slashes=False)
def index() -> jsonify:
    """the function of the url / that handles requests to that"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'],
           strict_slashes=False)
def users() -> jsonify:
    """gets two things, the email and the password which are used for
    authentication or to create a user if they do not exist"""
    email: str = request.form['email']
    password: str = request.form['password']
    try:
        user: User = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already exists"}), 400


@app.route('/sessions', methods=['POST'],
           strict_slashes=False)
def login() -> jsonify:
    """function that handles all the data related to logging in of
    users using their email addresses and passwords"""
    email: str = request.form['email']
    password: str = request.form['password']

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id: str = AUTH.create_session(email)
    response: jsonify = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response, 200


@app.route('/sessions', methods=['DELETE'],
           strict_slashes=False)
def logout() -> redirect:
    """function that is responsible for logging out and deleting a
    given session"""
    session_id: str = request.cookies.get("session_id")
    user: User = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'],
           strict_slashes=False)
def profile() -> jsonify:
    """the endpoint for creating a profile for a user"""
    session_id: str = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user: User = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'],
           strict_slashes=False)
def get_reset_password_token() -> jsonify:
    """route that handles reseting of a password"""
    email: str = request.form['email']
    try:
        reset_token: str = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'],
           strict_slashes=False)
def update_password() -> jsonify:
    """route that updates the password when the reset_token is
    available"""
    email: str = request.form['email']
    reset_token: str = request.form['reset_token']
    new_password = request.form['new_password']
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
