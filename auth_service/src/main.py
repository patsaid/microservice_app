"""
This module contains the main FastAPI application instance and the
API routes for the authentication service.
"""

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .crud import create_user, get_user_by_username
from .database import Base, engine, get_db
from .jwt import create_access_token, verify_password
from .logger import setup_logger
from .schemas import Token, UserCreate, UserOut

app = FastAPI()
logger = setup_logger()
Base.metadata.create_all(bind=engine)


@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (schemas.UserCreate): The user data to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        The created user.

    Raises:
        HTTPException: If the username is already registered.
    """
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        logger.error("Username already registered")
        raise HTTPException(status_code=400, detail="Username already registered")

    logger.info("User created successfully")
    return create_user(db, user=user)


@app.post("/authenticate", response_model=Token, status_code=status.HTTP_200_OK)
def authenticate(user: UserCreate, db: Session = Depends(get_db)):
    """
    Authenticates a user and generates an access token.

    Args:
        user (UserCreate): The user credentials.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the username or password is incorrect.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    db_user = get_user_by_username(db, username=user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        logger.error("Incorrect username or password")
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": db_user.username, "user_id": str(db_user.id)}
    )
    logger.info("User authenticated successfully")
    return {"access_token": access_token, "token_type": "bearer"}
