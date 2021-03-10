#!/usr/bin/env python

"""Main program."""

from page_loader.cli import get_input_params


def main():
    """Start CLI-program page loader."""
    output_dir, url = get_input_params()
    print(output_dir, url)


if __name__ == '__main__':
    main()
