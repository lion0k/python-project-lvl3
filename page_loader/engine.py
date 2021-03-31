"""Page loader engine."""

import logging
import os
from typing import Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from page_loader.file import (
    MAX_LENGTH_FILENAME,
    add_version,
    build_dirname,
    build_filename,
    convert_name,
    create_directory,
    write_file,
)
from progress.bar import Bar


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
    content = send_request(url).text
    resources_dir_name = build_dirname(url)
    root_dir = root_dir or os.getcwd()
    create_directory(root_dir, resources_dir_name)
    page, resources = parse_page(content, url, resources_dir_name)
    full_path_index_page = os.path.join(
        root_dir,
        '{name}.html'.format(name=convert_name(url)),
    )
    write_file(path=full_path_index_page, data=page)

    with Bar('Processing', max=len(resources)) as bar:
        for link, path in resources.items():
            bar.next()
            try:
                resource_content = send_request(link).content
            except requests.RequestException as error:
                logging.warning(error)
            else:
                write_file(os.path.join(root_dir, path), resource_content)

    return full_path_index_page


def parse_page(page: str, url: str, resources_dir: str) -> Tuple[str, dict]:
    """
    Parse page.

    Args:
        page: page
        url: URL
        resources_dir: directory name for resources

    Returns:
        tuple: parsed page, dict resources
    """
    soup = BeautifulSoup(page, 'html.parser')
    tags = {'img': 'src', 'script': 'src', 'link': 'href'}
    resources_links = {}
    file_versions = {}
    for tag in soup.find_all(tags):
        attr_value = tag.get(tags[tag.name])
        if attr_value is None:
            continue

        source_link = build_link(url, attr_value)
        if source_link is None:
            continue

        resources_filename = build_filename(source_link)
        if len(resources_filename) == MAX_LENGTH_FILENAME:
            exists_file_names = map(
                lambda file_name: file_name[1],
                map(os.path.split, resources_links.values()),
            )
            if resources_filename in exists_file_names:
                if resources_filename in file_versions:
                    file_versions[resources_filename] += 1
                else:
                    file_versions.setdefault(resources_filename, 0)
                resources_filename = add_version(
                    resources_filename,
                    file_versions[resources_filename],
                )

        resources_path = os.path.join(
            resources_dir,
            resources_filename,
        )

        tag[tags[tag.name]] = resources_path
        resources_links[source_link] = resources_path

        logging.debug('Link resources successful added {link}'.format(
            link=source_link,
        ))
    return soup.prettify(formatter='html5'), resources_links


def send_request(url: str) -> requests.Response:
    """
    Send request to url.

    Args:
        url: url

    Returns:
        Response:
    """
    response = requests.get(url)
    response.raise_for_status()

    return response
