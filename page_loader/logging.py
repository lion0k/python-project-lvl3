"""Logging."""

import logging

LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'


def config_logger(log_level):
    """
    Config setting logger.

    Args:
        log_level: level logger
    """
    logging.basicConfig(
        format=LOG_FORMAT,
        level=logging.getLevelName(log_level),
    )
