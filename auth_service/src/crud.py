"""
This module contains the CRUD operations for the User model.

The username is encrypted before storing it in the database and
decrypted when retrieving it for testing purposes.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session

from .config import DB_ENCRYPTION_KEY
from .jwt import hash_password
from .models import User
from .schemas import UserCreate


def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Parameters:
    - db (Session): The database session.
    - user (UserCreate): The user data to be created.

    Returns:
    - User: The created user object.
    """

    # Encrypt the username before storing it
    encrypted_username = db.execute(
        text("SELECT pgp_sym_encrypt(:username, :key)"),
        {"username": user.username, "key": DB_ENCRYPTION_KEY},
    ).scalar()

    db_user = User(
        username=encrypted_username,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Decrypt the username after retrieving it
    decrypted_username = db.execute(
        text("SELECT pgp_sym_decrypt(:encrypted_username, :key)"),
        {"encrypted_username": db_user.username, "key": DB_ENCRYPTION_KEY},
    ).scalar()

    db_user.username = decrypted_username

    return db_user


def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user from the database by their username.

    Args:
        db (Session): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        User: The user object if found, None otherwise.
    """

    result = db.execute(
        text(
            """
            SELECT id, 
                   pgp_sym_decrypt(username, :key) AS decrypted_username, 
                   hashed_password
            FROM users
            WHERE pgp_sym_decrypt(username, :key) = :username
        """
        ),
        {"key": DB_ENCRYPTION_KEY, "username": username},
    ).fetchone()

    if result:
        return User(id=result[0], username=result[1], hashed_password=result[2])

    return None
