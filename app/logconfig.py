import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name):
    """Set up a logger for the given name."""
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Set the logging level

    # Create handlers (console and file handlers)
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(
        'main.log', maxBytes=1024*1024*5, backupCount=5
    )

    # Create formatters and add them to handlers
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)

    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
