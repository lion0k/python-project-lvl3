#!/usr/bin/env python

"""Main program."""

from sys import exit

from page_loader.cli import get_input_params
from page_loader.engine import download
from page_loader.logging import KnownError, config_logger


def main():
    """Start CLI-program page loader."""
    output_dir, url, log_level = get_input_params()
    config_logger(log_level)
    try:
        print(download(url, output_dir))
    except KnownError:
        exit(1)


if __name__ == '__main__':
    main()
