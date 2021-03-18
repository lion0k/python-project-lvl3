"""Page loader engine."""

import logging
from collections import namedtuple
from contextlib import suppress
from os.path import join
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup as Bs
from page_loader.file import (
    build_filename,
    convert_name,
    create_directory,
    write_file,
)
from page_loader.logging import KnownError
from progress.bar import Bar
from requests import get
from requests.exceptions import RequestException

ERROR_LOAD = "Code '{error}'. The data at this address '{url}' was not loaded."
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
    page, resources = parse_page(send_request(url), url, resources_dir)
    full_path_index_page = join(root_dir, page_name)
    write_file(
        path=full_path_index_page,
        data=page,
    )
    with Bar('Processing', max=len(resources)) as bar:
        for resource in resources:
            bar.next()
            with suppress(RequestException, OSError):
                write_file(
                    resource['path'],
                    send_request(resource['link']),
                )
    return full_path_index_page


def parse_page(page: str, url: str, resources_dir_name: str) -> tuple:
    """
    Parse page.

    Args:
        page: page
        url: URL
        resources_dir_name: directory name for resources

    Returns:
        tuple: parsed page, list resources
    """
    parse_url_root = parse_url(url)
    soup = Bs(page, 'html5lib')
    tags = {'img': 'src', 'script': 'src', 'link': 'href'}
    resources_links = []
    unique_links = set()
    for tag in soup.find_all(tags):
        attr_value = tag.get(tags[tag.name])
        if attr_value is None:
            continue

        parse_url_source = parse_url(attr_value)
        if not parse_url_source.netloc:
            source_link = urljoin(url, attr_value)
        elif parse_url_root.netloc == parse_url_source.netloc:
            source_link = attr_value
        else:
            continue

        changed_link = join(
            resources_dir_name,
            build_filename(parse_url_root, parse_url_source),
        )
        tag[tags[tag.name]] = '{source}'.format(source=changed_link)

        if source_link in unique_links:
            continue
        unique_links.add(source_link)

        resources_links.append({
            'path': join(resources_dir_name, changed_link),
            'link': source_link,
        })

        logging.debug('Link resources successful added {link}'.format(
            link=source_link,
        ))
    return soup.encode(formatter='html5'), resources_links


def parse_url(url: str) -> namedtuple:
    """
    Parse url.

    Args:
        url: URL

    Returns:
        namedtuple: include parsed 'scheme, 'netloc', 'path'
    """
    url_parse = urlparse(url)
    return namedtuple('URL', ['scheme', 'netloc', 'path'])(
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
        KnownError: masking RequestException, HTTPError

    Returns:
        any:
    """
    try:
        response = get(url)
    except RequestException as error:
        logging.error(error)
        raise KnownError(error)

    if response.status_code != SUCCESSFUL_STATUS_CODE:
        logging.warning(ERROR_LOAD.format(
            url=url,
            error=response.status_code,
        ))
        response.raise_for_status()

    return response.content
