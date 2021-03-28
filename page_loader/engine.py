"""Page loader engine."""

import logging
from os.path import join
from typing import Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from page_loader.file import (
    build_dirname,
    build_filename,
    convert_name,
    create_directory,
    write_file,
)
from progress.bar import Bar
from requests import Response, get
from requests.exceptions import RequestException


def build_link(root_url: str, source_url: str) -> Optional[str]:
    """
    Build correct link.

    Args:
        root_url: root URL
        source_url: source URL

    Returns:
        optional:
    """
    parsed_root_url = urlparse(root_url)
    parsed_source_url = urlparse(source_url)
    root_netloc = parsed_root_url.netloc
    source_netloc = parsed_source_url.netloc
    if not source_netloc or root_netloc == source_netloc:
        return urljoin(root_url, source_url)


def download(url: str, root_dir: str) -> str:
    """
    Download page from URL.

    Args:
        url: URL
        root_dir: directory to download

    Returns:
        str:
    """
    content = send_request(url).content
    resources_dir_name = build_dirname(url)
    create_directory(
        root_dir,
        resources_dir_name,
    )
    page, resources = parse_page(content, url, resources_dir_name)
    full_path_index_page = join(
        root_dir,
        '{name}.html'.format(name=convert_name(url)),
    )
    write_file(path=full_path_index_page, data=page)

    with Bar('Processing', max=len(resources)) as bar:
        for link, path in resources.items():
            bar.next()
            try:
                write_file(
                    join(root_dir, path),
                    send_request(link).content,
                )
            except RequestException as error:
                logging.warning(error)
    return full_path_index_page


def parse_page(page: bytes, url: str, resources_dir_name: str) -> tuple:
    """
    Parse page.

    Args:
        page: page
        url: URL
        resources_dir_name: directory name for resources

    Returns:
        tuple: parsed page, list resources
    """
    soup = BeautifulSoup(page, 'html.parser')
    tags = {'img': 'src', 'script': 'src', 'link': 'href'}
    resources_links = {}
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
        tag[tags[tag.name]] = changed_link
        resources_links[source_link] = changed_link

        logging.debug('Link resources successful added {link}'.format(
            link=source_link,
        ))
    return soup.prettify(formatter='html5'), resources_links


def send_request(url: str) -> Response:
    """
    Send request to url.

    Args:
        url: url

    Raises:
        RequestException: RequestException

    Returns:
        Response:
    """
    try:
        response = get(url)
    except RequestException as error:
        raise RequestException(error)

    return response
