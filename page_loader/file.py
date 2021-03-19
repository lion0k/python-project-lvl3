"""File functions."""

import logging
from os import mkdir
from os.path import join, splitext
from re import sub
from urllib.parse import urlparse, urlunparse

from page_loader.logging import KnownError

MAX_LENGTH_FILENAME = 250


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


def build_filename(root_url: str, source_url: str) -> str:
    """
    Build filename.

    Args:
        root_url: root URL
        source_url: source URL

    Returns:
        str:
    """
    parsed_root_url = urlparse(root_url)
    parsed_source_url = urlparse(source_url)
    path, extension = splitext(parsed_source_url.path)
    changed_name = parsed_source_url._replace(
        scheme=parsed_root_url.scheme,
        netloc=parsed_root_url.netloc,
        path=path,
    )
    name = convert_name(urlunparse(changed_name))
    length_name = len(name) + len(extension)
    if length_name > MAX_LENGTH_FILENAME:
        name = name[:length_name - (length_name - MAX_LENGTH_FILENAME)]

    return '{name}{extension}'.format(
        name=name,
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
