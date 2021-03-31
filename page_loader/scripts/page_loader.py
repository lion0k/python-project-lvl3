#!/usr/bin/env python

"""Main program."""

import logging
from sys import exit

from page_loader.cli import get_input_params
from page_loader.engine import download
from page_loader.logging import config_logger


def main():
    """Start CLI-program page loader."""
    args = get_input_params()
    config_logger(args.log)
    try:
        print(download(args.url, args.output))
    except Exception as error:
        logging.exception(error)
        exit(1)


if __name__ == '__main__':
    main()
