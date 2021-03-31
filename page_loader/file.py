"""File functions."""

import logging
import os
import re
from typing import Union
from urllib.parse import urljoin, urlparse

MAX_LENGTH_FILENAME = 255
PATTERN_SCHEME = re.compile('(^.+://)')
PATTERN_PATH = re.compile('([^a-zA-Z0-9]+)')


def create_directory(path: str, name_folder: str):
    """
    Create directory.

    Args:
        path: full path
        name_folder: name folder
    """
    abs_path = os.path.join(path, name_folder)
    os.mkdir(abs_path)

    logging.debug('Successful create directory {path}'.format(
        path=abs_path,
    ))


def write_file(path: str, data: Union[str, bytes]):
    """
    Write file.

    Args:
        path: full path
        data: data
    """
    mode = 'w' if isinstance(data, str) else 'wb'
    with open(path, mode) as file_descriptor:
        file_descriptor.write(data)

    logging.debug('Successful write file {path}'.format(
        path=path,
    ))


def build_filename(url: str) -> str:
    """
    Build filename.

    Args:
        url: URL

    Returns:
        str:
    """
    parsed_url = urlparse(url)
    path, extension = os.path.splitext(parsed_url.path)
    name = convert_name(urljoin(url, path))
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
    url_without_scheme = PATTERN_SCHEME.sub('', url)
    return PATTERN_PATH.sub('-', url_without_scheme)


def add_version(filename: str, version: int) -> str:
    """
    Add version in filename.

    Args:
        filename: filename
        version: version

    Returns:
        str:
    """
    path, extension = os.path.splitext(filename)
    crop_path = path[:len(path) - len(str(version))]
    return '{crop_path}{version}{extension}'.format(
        crop_path=crop_path,
        version=version,
        extension=extension,
    )
