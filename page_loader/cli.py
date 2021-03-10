"""Command line interface."""

import argparse
from os import getcwd


def get_input_params() -> tuple:
    """
    Get input params.

    Returns:
        tuple: tuple with input arguments
    """
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument(
        'url',
        type=str,
        help='URL to target page',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default=getcwd(),
        help='set directory for saved pages (default: current directory)',
    )
    args = parser.parse_args()
    return args.output, args.url
