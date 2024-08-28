"""
This module contains the schema classes for the application.
"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    UserCreate schema class.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    username: str
    password: str


class UserOut(BaseModel):
    """
    UserOut schema class.

    Attributes:
        id (int): The user ID.
        username (str): The username.
    """

    id: int
    username: str

    class Config:
        """
        Pydantic configuration class.
        """

        from_attributes = True


class Token(BaseModel):
    """
    Represents a token object.

    Attributes:
        access_token (str): The access token.
        token_type (str): The type of the token.
    """

    access_token: str
    token_type: str
