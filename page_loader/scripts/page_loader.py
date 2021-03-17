#!/usr/bin/env python

"""Main program."""

from page_loader.cli import get_input_params
from page_loader.engine import download
from page_loader.log import config_logger


def main():
    """Start CLI-program page loader."""
    output_dir, url, log_level = get_input_params()
    config_logger(log_level)
    print(download(output_dir, url))


if __name__ == '__main__':
    main()
