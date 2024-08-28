"""
This module contains the main FastAPI application for the Coordinator Service.

"""

import base64
import json
from typing import Dict

import httpx
import pika
from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel

from .config import AUTH_SERVICE_URL, RABBITMQ_HOST
from .logger import setup_logger

app = FastAPI()
logger = setup_logger()


# Define Pydantic models for request payload
class UserCreate(BaseModel):
    """
    Represents a user creation request.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
    """

    username: str
    password: str


class UserResponse(BaseModel):
    """
    Represents a user response.

    Attributes:
        id (str): The user's ID.
        username (str): The user's username.
        email (str): The user's email address.
    """

    id: int
    username: str


def send_task_to_rabbitmq(task_data, jwt_token):
    """
    Sends a task to RabbitMQ with the JWT token included in the payload.

    Args:
        task_data (dict): The data of the task to be sent.
        jwt_token (str): The JWT token to be included in the task payload.

    Returns:
        None
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue="product_tasks")

    # Include the token in the task payload
    payload = {"task": task_data, "token": jwt_token}

    channel.basic_publish(
        exchange="", routing_key="product_tasks", body=json.dumps(payload)
    )
    connection.close()


def parse_basic_auth_header(auth_header: str) -> Dict[str, str]:
    """
    Parses the Basic Authorization header and returns a dictionary containing the username
    and password.

    Args:
        auth_header (str): The Basic Authorization header string.

    Returns:
        Dict[str, str]: A dictionary containing the username and password extracted from
        the header.

    Raises:
        HTTPException: If the authorization header is invalid.
    """
    if not auth_header.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    try:
        # Extract the Base64 encoded part
        encoded_credentials = auth_header[len("Basic ") :]
        # Decode the Base64 encoded credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        # Split the credentials into username and password
        username, password = decoded_credentials.split(":", 1)
        return {"username": username, "password": password}
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Invalid authorization header"
        ) from e


@app.post("/process", status_code=status.HTTP_202_ACCEPTED)
async def process_request(
    request: Request,
    request_data: dict,
):
    """
    Process the incoming request by authenticating the request data with the authentication
    service. If authentication is successful, send the task to RabbitMQ with the JWT token
    included in the payload and return a success response. If authentication fails, raise
    an HTTPException with a status code of 401.

    Parameters:
    - additional_data (RequestData, optional): The additional data of the incoming request.
    - Username (str): The username for authentication (provided in headers).
    - Password (str): The password for authentication (provided in headers).

    Returns:
    - dict: A dictionary containing the status of the request.

    Raises:
    - HTTPException: If the authentication fails.
    """

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    credentials = parse_basic_auth_header(auth_header)
    username = credentials["username"]
    password = credentials["password"]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AUTH_SERVICE_URL}/authenticate",
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            # Authentication successful, get the JWT token
            jwt_token = response.json().get("access_token")
            if not jwt_token:
                raise HTTPException(status_code=500, detail="No access token returned")

            # Send task to RabbitMQ with JWT token
            send_task_to_rabbitmq(request_data, jwt_token)
            logger.info("Task sent to RabbitMQ")
            return {"status": "success"}
        else:
            logger.error("Authentication failed")
            raise HTTPException(status_code=401, detail="Authentication failed")


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """
    Register a new user by sending a request to the auth service.

    Args:
        user (UserCreate): The user data to be registered.

    Returns:
        UserResponse: The registered user data.

    Raises:
        HTTPException: If the registration fails.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AUTH_SERVICE_URL}/register", json=user.model_dump()
        )
        if response.status_code == 201:
            # Registration successful, return user data
            logger.info("User registered successfully")
            return response.json()
        else:
            logger.error("User registration failed")
            raise HTTPException(
                status_code=response.status_code, detail="User registration failed"
            )
