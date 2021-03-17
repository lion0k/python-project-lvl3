"""Logging."""

import logging
import sys


def config_logger(log_level):
    """
    Config setting logger.

    Args:
        log_level: level logger
    """
    stdout_handler = logging.StreamHandler(sys.stdout)
    logger = logging.getLogger()

    formatter = logging.Formatter('{asctime}-{levelname}-{message}', style='{')
    stdout_handler.setFormatter(formatter)

    if log_level == 'warning':
        logger.setLevel(logging.WARNING)
    elif log_level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif log_level == 'error':
        logger.setLevel(logging.ERROR)
    logger.addHandler(stdout_handler)
