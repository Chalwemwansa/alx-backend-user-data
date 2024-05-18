#!/usr/bin/env python3
"""
Main file
"""
import bcrypt

hash_password = __import__('encrypt_password').hash_password

password = "MyAmazingPassw0rd"
print(hash_password(password))
hashed_password: bytes = hash_password(password)
print(bcrypt.checkpw(password.encode('utf-8'), hashed_password))
