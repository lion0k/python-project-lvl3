"""Command line interface."""

from argparse import ArgumentParser, Namespace
from os import getcwd


def get_input_params() -> Namespace:
    """
    Get input params.

    Returns:
        Namespace: parsed arguments
    """
    parser = ArgumentParser(description='Page loader')
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
    parser.add_argument(
        '-l',
        '--log',
        type=str,
        default='error',
        choices=['error', 'warning', 'debug'],
        help='set the logging level (default: error)',
    )
    return parser.parse_args()
