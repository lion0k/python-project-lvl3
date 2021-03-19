"""Logging."""

import logging
import sys


class KnownError(Exception):
    """Known exception."""

    pass


def config_logger(log_level):
    """
    Config setting logger.

    Args:
        log_level: level logger
    """
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    logger = logging.getLogger()

    formatter = logging.Formatter(
        '{asctime}-{levelname}-{message}',
        style='{',
    )
    stdout_handler.setFormatter(formatter)

    if log_level == 'warning':
        logger.setLevel(logging.WARNING)
        logger.addHandler(stdout_handler)
    elif log_level == 'debug':
        logger.setLevel(logging.DEBUG)
        logger.addHandler(stdout_handler)
    elif log_level == 'error':
        logger.setLevel(logging.ERROR)
        logger.addHandler(stderr_handler)
