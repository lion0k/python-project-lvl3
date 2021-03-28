"""File functions."""

import logging
import re
from os import mkdir
from os.path import join, splitext
from urllib.parse import urlparse, urlunparse

MAX_LENGTH_FILENAME = 255


def create_directory(path: str, name_folder: str):
    """
    Create directory.

    Args:
        path: full path
        name_folder: name folder

    Raises:
        OSError: OSError
    """
    abs_path = join(path, name_folder)
    try:
        mkdir(abs_path)
    except OSError as error:
        raise OSError(error)

    logging.debug('Successful create directory {path}'.format(
        path=abs_path,
    ))


def write_file(path: str, data: bytes):
    """
    Write file.

    Args:
        path: full path
        data: data

    Raises:
        OSError: OSError
    """
    mode = 'w' if isinstance(data, str) else 'wb'
    try:
        with open(path, mode) as file_descriptor:
            file_descriptor.write(data)
    except OSError as error:
        raise OSError(error)

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
    extension = extension if extension else '.html'
    if len(name) + len(extension) > MAX_LENGTH_FILENAME:
        name = name[:(MAX_LENGTH_FILENAME - len(extension))]

    return '{name}{extension}'.format(
        name=name,
        extension=extension,
    )


def build_dirname(url: str) -> str:
    """
    Build directory name.

    Args:
        url: URL

    Returns:
        str:
    """
    parsed_root_url = urlparse(url)
    return '{netloc}{path}_files'.format(
        netloc=convert_name(parsed_root_url.netloc),
        path=convert_name(parsed_root_url.path),
    )


def convert_name(url: str) -> str:
    """
    Convert name.

    Args:
        url: URL

    Returns:
        str:
    """
    pattern_scheme = re.compile('(^.+://)')
    pattern_not_word = re.compile('([^a-zA-Z0-9]+)')
    url_without_scheme = re.sub(pattern_scheme, '', url)
    return re.sub(pattern_not_word, '-', url_without_scheme)
