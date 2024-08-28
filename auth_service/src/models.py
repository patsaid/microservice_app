"""
This module contains the database models for the application.
"""

from sqlalchemy import Column, Integer, LargeBinary, String

from .database import Base


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        hashed_password (str): The hashed password of the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(LargeBinary, unique=True, index=True)
    hashed_password = Column(String)
