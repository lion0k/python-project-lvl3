"""Page loader engine."""

import logging
from contextlib import suppress
from os.path import join
from urllib.parse import urlparse, urlunparse

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


def build_link(root_url: str, source_url: str) -> str:
    """
    Build correct link.

    Args:
        root_url: root URL
        source_url: source URL

    Returns:
        str:
    """
    parsed_root_url = urlparse(root_url)
    parsed_source_url = urlparse(source_url)
    root_netloc = parsed_root_url.netloc
    source_netloc = parsed_source_url.netloc
    if not source_netloc or root_netloc == source_netloc:
        change_url = parsed_source_url._replace(
            scheme=parsed_root_url.scheme,
            netloc=parsed_root_url.netloc,
        )
        return urlunparse(change_url)


def download(url: str, root_dir: str) -> str:
    """
    Download page from URL.

    Args:
        url: URL
        root_dir: directory to download

    Returns:
        str:
    """
    content = send_request(url)

    parsed_root_url = urlparse(url)
    resources_dir_name = '{netloc}{path}_files'.format(
        netloc=convert_name(parsed_root_url.netloc),
        path=convert_name(parsed_root_url.path),
    )
    create_directory(
        root_dir,
        resources_dir_name,
    )
    page, resources = parse_page(content, url, resources_dir_name)
    full_path_index_page = join(root_dir, build_filename(url, url))
    write_file(path=full_path_index_page, data=page)

    with Bar('Processing', max=len(resources)) as bar:
        for resource in resources:
            bar.next()
            with suppress(RequestException, OSError):
                write_file(
                    join(root_dir, resource['path']),
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
    soup = Bs(page, 'html5lib')
    tags = {'img': 'src', 'script': 'src', 'link': 'href'}
    resources_links = []
    unique_links = set()
    for tag in soup.find_all(tags):
        attr_value = tag.get(tags[tag.name])
        if attr_value is None:
            continue

        source_link = build_link(url, attr_value)
        if source_link is None:
            continue

        changed_link = join(
            resources_dir_name,
            build_filename(url, attr_value),
        )
        tag[tags[tag.name]] = '{source}'.format(source=changed_link)

        if source_link in unique_links:
            continue
        unique_links.add(source_link)

        resources_links.append({
            'path': changed_link,
            'link': source_link,
        })

        logging.debug('Link resources successful added {link}'.format(
            link=source_link,
        ))
    return soup.encode(formatter='html5'), resources_links


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
