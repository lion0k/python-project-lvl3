#!/usr/bin/env python

"""Main program."""

from page_loader.cli import get_input_params
from page_loader.engine import download


def main():
    """Start CLI-program page loader."""
    output_dir, url = get_input_params()
    print(download(output_dir, url))


if __name__ == '__main__':
    main()
