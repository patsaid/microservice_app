"""
This module initializes the RabbitMQ consumer and starts consuming messages.
"""

import json
import time

import pika
import sqlalchemy
from jose import JWTError, jwt
from sqlalchemy.orm import sessionmaker

from .config import (
    DATABASE_URL,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    RABBITMQ_HOST,
    RABBITMQ_PORT,
)
from .logger import setup_logger
from .models import Base, Product

logger = setup_logger()


def create_rabbitmq_connection():
    """
    Creates a RabbitMQ connection.

    This function attempts to establish a connection to a RabbitMQ server using the pika library.
    It continuously retries the connection until it is successful.

    Returns:
        pika.BlockingConnection: The established RabbitMQ connection.

    Raises:
        pika.exceptions.AMQPConnectionError: If the connection to the RabbitMQ server fails.
    """

    while True:
        try:
            conn = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
            )
            return conn
        except pika.exceptions.AMQPConnectionError:
            print("Connection failed, retrying...")
            time.sleep(5)  # Wait before retrying


def verify_token(token: str) -> dict:
    """
    Verifies a JWT token.

    Args:
        token (str): The JWT token to be verified.

    Returns:
        dict: The decoded payload if the token is valid.

    Raises:
        ValueError: If the token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as exc:
        raise ValueError("Invalid token") from exc


# Setup SQLAlchemy
engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
logger.info("Database setup complete.")

# Setup RabbitMQ
connection = create_rabbitmq_connection()
channel = connection.channel()
channel.queue_declare(queue="product_tasks")
logger.info("RabbitMQ setup complete and queue declared.")


def callback(ch, method, properties, body):
    """
    Callback function for processing incoming messages.

    Args:
        ch: The channel object.
        method: The method object.
        properties: The properties object.
        body: The message body.

    Returns:
        None
    """
    task = body.decode()
    logger.info("Received a new task.")

    # Extract and verify the token
    try:
        task_data = json.loads(task)
        data = task_data.get("task")
        token = task_data.get("token")
        if token:
            verify_token(token)  # Validate the token
        else:
            logger.warning("No token provided. Task cannot be processed.")
            return

        # Proceed with processing if token is valid
        product_item = Product(
            name=data["name"],
            description=data["description"],
            price=data["price"],
        )

        db = SessionLocal()
        db.add(product_item)
        db.commit()
        logger.info("Product '%s' added to the database.", product_item.name)
        db.close()
    except ValueError as e:
        logger.error("Token validation failed: %s", e)


channel.basic_consume(
    queue="product_tasks", on_message_callback=callback, auto_ack=True
)
logger.info("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
