"""
This module initializes New Relic, creates a custom logging handler,
and configures the logging for the application.
"""

import logging
import os

import newrelic.agent

# Initialize New Relic
newrelic.agent.initialize(os.path.join(os.path.dirname(__file__), "newrelic.ini"))
application = newrelic.agent.register_application(timeout=10)


class NewRelicHandler(logging.Handler):
    """
    Emit a log record to New Relic.

    Args:
        record (logging.LogRecord): The log record to emit.

    Returns:
        None
    """

    def emit(self, record):
        log_entry = self.format(record)
        newrelic.agent.record_custom_event(
            "LogEvent",
            {"level": record.levelname, "message": log_entry},
            application=application,
        )


def setup_logger():
    """
    Set up the logger with the specified log level and handlers.

    Returns:
        logger (logging.Logger): The configured logger object.
    """
    # Get log level from environment variable or default to INFO
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, log_level, logging.INFO)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create handlers
    new_relic_handler = NewRelicHandler()
    new_relic_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers = []  # Clear any existing handlers

    # Add handlers to the root logger
    logger.addHandler(new_relic_handler)
    logger.addHandler(console_handler)

    return logger
