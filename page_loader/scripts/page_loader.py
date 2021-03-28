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
    output_dir, url, log_level = tuple(map(
        lambda arg: arg.lower(),
        [args.output, args.url, args.log],
    ))
    config_logger(log_level)
    try:
        print(download(url, output_dir))
    except Exception as error:
        logging.error(error)
        exit(1)


if __name__ == '__main__':
    main()
