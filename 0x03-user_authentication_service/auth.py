#!/usr/bin/env python3
"""module contains the auth class that is responsible for
authentication"""
import bcrypt
from sqlalchemy.orm import UserDefinedOption
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from typing import Optional


def _hash_password(password: str) -> bytes:
    """hashes a password and returns the hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """the auth class that contains inplementation of
    authentication methods"""

    def __init__(self):
        """the constructor method for the class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """the method that registers a user by hashing the password
        and raising a value error if user already exists"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            user: User = self._db.add_user(email, _hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """function validates a user before logging in to check if user is
         legit"""
        try:
            user: User = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """function creates a new uuid and returns a string version of it"""
        import uuid

        return str(uuid.uuid4())

    def create_session(self, email: str) -> Optional[str]:
        """function takes in a string email as an argument and returns
        the session id in form of a string as a return"""
        try:
            user: User = self._db.find_user_by(email=email)
            user.session_id = self._generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: Optional[str])\
            -> Optional[User]:
        """function gets as a sring the session id and returns the user
        belonging to that session"""
        if session_id is None:
            return None
        try:
            user: User = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """function is responsible for destroying a session for the
        id passed as an argument"""
        try:
            user: User = self._db.find_user_by(id=user_id)
            user.session_id = None
            return user.session_id
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """function that resets the password for the user related to
        the email passed as an argument"""
        try:
            user: User = self._db.find_user_by(email=email)
            user.reset_token = self._generate_uuid()
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(reset_token: str, password: str) -> None:
        """function resets the password of a user and returns None"""
        try:
            user: User = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(password)
            user.reset_token = None
        except NoResultFound:
            raise ValueError
