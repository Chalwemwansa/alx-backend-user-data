#!/usr/bin/env python3
"""this module contains the db class that is used by
python to interact with the database"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Type, Dict

from user import Base, User


class DB:
    """DB class that is responsible for interaction with database
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """the function that creates a new user and adds
        the userto the db"""
        user: User = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """returns the first row found in the database
         where a user with the given parameters is found"""
        return self._session.query(User).filter_by(**kwargs).one()

    def update_user(self, user_id: int, **kwargs: Dict[str, str]) -> None:
        """updates the user with the given id with the given parameters"""
        user: User = self.find_user_by(id=user_id)
        valid: List[str] = ["id", "email", "hashed_password",
                            "session_id", "reset_token"]
        for key, value in kwargs.items():
            if key not in valid:
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
