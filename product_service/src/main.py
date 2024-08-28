"""
This module initializes the RabbitMQ consumer and starts consuming messages.
"""

from .consumer import channel
from .logger import setup_logger

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Starting RabbitMQ consumer...")
    channel.start_consuming()
