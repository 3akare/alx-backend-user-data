#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
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
        """
        Adds new user to the database
        """
        try:
            nuser = User(email=email, hashed_password=hashed_password)
            self._session.add(nuser)
            self._session.commit()
        except Exception:
            self._session.rollback()
            nuser = None
        return nuser

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user based on a set of filters.
        """
        query = self._session.query(User)
        for key, value in kwargs.items():
            if hasattr(User, key):
                query = query.filter(getattr(User, key) == value)
            else:
                raise InvalidRequestError()
        result = query.first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update user by user_id
        """
        try:
            user = self.find_user_by(id=user_id)
            if user is None:
                return
            self._session.query(User).filter(User.id == user_id).update(kwargs)
            return None
        except (InvalidRequestError, NoResultFound, NameError):
            raise ValueError
