#!/usr/bin/env python3
"""this script makes an ORM table using sqlalchemy in python"""
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from typing import Type, Dict, Union, Optional


Base: Type[DeclarativeMeta] = declarative_base()


class User(Base):
    """the user class that inherits from declarative to
    create a table called users in the database"""
    __tablename__: str = "users"

    id: Optional[int] = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: Optional[str] = Column(String(250), nullable=True)
    reset_token: Optional[str] = Column(String(250), nullable=True)

    def __init__(self, **kwargs: Dict[str, Union[int, str, None]]) -> None:
        """initialize the user instance"""
        if kwargs.get("id"):
            self.id = kwargs.get("id")
        if kwargs.get("email"):
            self.email = kwargs.get("email")
        if kwargs.get("hashed_password"):
            self.hashed_password = kwargs.get("hashed_password")
        if kwargs.get("session_id"):
            self.session_id = kwargs.get("session_id")
        if kwargs.get("reset_token"):
            self.reset_token = kwargs.get("reset_token")
