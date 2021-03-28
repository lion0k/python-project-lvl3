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
    stderr_handler = logging.StreamHandler(sys.stderr)
    logger = logging.getLogger()

    formatter = logging.Formatter(
        '{asctime}-{levelname}-{message}',
        style='{',
    )
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)

    levels = {
        'warning': logging.WARNING,
        'debug': logging.DEBUG,
        'error': logging.ERROR,
    }
    logger.setLevel(levels[log_level])
    if logging.getLevelName(levels[log_level]) == levels[log_level]:
        logger.addHandler(stderr_handler)
    else:
        logger.addHandler(stdout_handler)
