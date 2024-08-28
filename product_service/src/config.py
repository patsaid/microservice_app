"""
This module contains the configuration settings for the application.
"""

from decouple import config

# Define PostgreSQL settings
DATABASE_URL = config("DATABASE_URL")

# Define RabbitMQ settings
RABBITMQ_HOST = config("RABBITMQ_HOST")
RABBITMQ_PORT = config("RABBITMQ_PORT")

# Define JWT settings
JWT_SECRET_KEY = config("JWT_SECRET_KEY")
JWT_ALGORITHM = config("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
