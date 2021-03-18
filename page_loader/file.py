"""File functions."""

import logging
from collections import namedtuple
from os import mkdir
from os.path import join, splitext
from re import sub
from urllib.parse import urljoin

from page_loader.logging import KnownError


def create_directory(path: str, name_folder: str) -> str:
    """
    Create directory.

    Args:
        path: full path
        name_folder: name folder

    Raises:
        KnownError: masking OSError, PermissionError

    Returns:
        str: full path to created directory
    """
    abs_path = join(path, name_folder)
    try:
        mkdir(abs_path)
    except OSError as error:
        logging.error(error)
        raise KnownError(error)

    logging.debug('Successful create directory {path}'.format(
        path=abs_path,
    ))
    return abs_path


def write_file(path: str, data):
    """
    Write file.

    Args:
        path: full path
        data: data

    Raises:
        KnownError: masking OSError, PermissionError
    """
    try:
        with open(path, 'wb') as file_descriptor:
            file_descriptor.write(data)
    except OSError as error:
        logging.error(error)
        raise KnownError(error)

    logging.debug('Successful write file {path}'.format(
        path=path,
    ))


def build_filename(root_url: namedtuple, source_url: namedtuple) -> str:
    """
    Build filename.

    Args:
        root_url: parsed root URL
        source_url: parsed source URL

    Returns:
        str:
    """
    path, extension = splitext(source_url.path)
    changed_name = convert_name(urljoin(
        '{scheme}://{netloc}'.format(
            scheme=root_url.scheme,
            netloc=root_url.netloc,
        ),
        path,
    ))
    return '{name}{extension}'.format(
        name=changed_name,
        extension=extension if extension else '.html',
    )


def convert_name(url: str) -> str:
    """
    Convert name.

    Args:
        url: URL

    Returns:
        str:
    """
    url_without_scheme = sub('(^.+://)', '', url)
    return sub('([^a-zA-Z0-9]+)', '-', url_without_scheme)
