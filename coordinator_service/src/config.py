"""
This module contains the configuration settings for the application.
"""

from decouple import config

# Define auth service settings
AUTH_SERVICE_URL = config("AUTH_SERVICE_URL")

# Define rabbitmq settings
RABBITMQ_HOST = config("RABBITMQ_HOST")
