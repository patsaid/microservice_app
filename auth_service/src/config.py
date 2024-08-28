"""
This module contains the configuration settings for the application.
"""

from decouple import config

# Define PostgreSQL settings
DATABASE_URL = config("DATABASE_URL")
DB_ENCRYPTION_KEY = config("DB_ENCRYPTION_KEY")

# Define JWT settings
JWT_SECRET_KEY = config("JWT_SECRET_KEY")
JWT_ALGORITHM = config("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
