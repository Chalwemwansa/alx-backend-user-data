#!/usr/bin/env python3
"""this module contains a function that is used to encrypt passwords
passed to it using bcypt haspow method"""
import bcrypt


def hash_password(password: str) -> bytes:
    """the function that hashes the string passed to it as an argument"""
    salt: bytes = bcrypt.gensalt()
    hashed_pasword: bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pasword


def is_valid(hashed_password: bytes, password: str) -> bool:
    """the is_valid function checks if the password
    passed to the function is the write password and returns
    a boolean value of True if it is the right password and False"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
