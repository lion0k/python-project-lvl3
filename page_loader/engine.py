"""Page loader engine."""

import logging
from collections import namedtuple
from contextlib import suppress
from os.path import join, splitext
from re import sub
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup as Bs
from page_loader.file import create_directory, write_file
from page_loader.logging import KnownError
from requests import get
from requests.exceptions import HTTPError, RequestException

ERROR_REQUEST = "The data at this address '{url}' was not loaded. Error-{error}"
SUCCESSFUL_STATUS_CODE = 200


def download(root_dir: str, url: str) -> str:
    """
    Download page from URL.

    Args:
        root_dir: directory to download
        url: URL

    Returns:
        str:
    """
    url_parse = parse_url(url)
    prepare_name = '{netloc}{path}'.format(
        netloc=convert_name(url_parse.netloc),
        path=convert_name(url_parse.path),
    )
    page_name = '{name}.html'.format(name=prepare_name)
    resources_dir_name = '{name}_files'.format(name=prepare_name)

    resources_dir = create_directory(
        root_dir,
        resources_dir_name,
    )
    page = parse_page(send_request(url), url, resources_dir)
    write_file(
        path=join(root_dir, page_name),
        data=page,
    )

    return join(root_dir, page_name)


def parse_page(page: str, url: str, resources_dir_name: str):
    """
    Parse page and downloads resources.

    Args:
        page: page
        url: URL
        resources_dir_name: directory name for resources

    Returns:
        any:
    """
    root_parse_url = parse_url(url)
    soup = Bs(page, 'html5lib')
    tags = {'img': 'src', 'script': 'src', 'link': 'href'}
    for tag in soup.find_all(tags):
        attr_value = tag.get(tags[tag.name])
        if attr_value is None:
            continue

        source_parse_url = parse_url(attr_value)
        if not source_parse_url.netloc:
            source_link = urljoin(url, attr_value)
        elif root_parse_url.netloc == source_parse_url.netloc:
            source_link = attr_value
        else:
            continue

        changed_name = build_filename(root_parse_url, source_parse_url)
        changed_link = join(
            resources_dir_name,
            changed_name,
        )

        with suppress(RequestException, HTTPError, OSError):
            write_file(
                join(resources_dir_name, changed_link),
                send_request(source_link),
            )
        logging.info('Successful load resources {link}'.format(
            link=source_link,
        ))

        tag[tags[tag.name]] = '{source}'.format(source=changed_link)
    return soup.encode(formatter='html5')


def parse_url(url: str) -> namedtuple:
    """
    Parse url.

    Args:
        url: URL

    Returns:
        namedtuple: include parsed 'scheme, 'netloc', 'path'
    """
    url_parse = urlparse(url)
    return namedtuple('Url', ['scheme', 'netloc', 'path'])(
        scheme=url_parse.scheme,
        netloc=url_parse.netloc,
        path=url_parse.path,
    )


def send_request(url: str):
    """
    Send request to url.

    Args:
        url: url

    Raises:
        KnownError: error send request

    Returns:
        any:
    """
    try:
        response = get(url)
    except RequestException as error:
        logging.error(error)
        raise KnownError(error)

    if response.status_code != SUCCESSFUL_STATUS_CODE:
        logging.warning(ERROR_REQUEST.format(
            url=url,
            error=response.status_code,
        ))
        response.raise_for_status()

    return response.content


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
