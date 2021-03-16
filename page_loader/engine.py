"""Page loader engine."""

from collections import namedtuple
from contextlib import suppress
from os.path import join
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup as Bs
from page_loader.file import convert_name, create_directory, write_file
from requests import get
from requests.exceptions import HTTPError, RequestException

ERROR_REQUEST = "\n\nThe data at this address '{url}' was not loaded.\n{error}"
SUCCESSFUL_STATUS_CODE = 200
TAGS = {
    'img': 'src',
}


def download(output_dir: str, url: str) -> str:
    """
    Download pages from URL with resources.

    Args:
        output_dir: directory to download
        url: URL

    Returns:
        str: full path to downloaded index page
    """
    return join(
        output_dir,
        download_page(output_dir, url),
    )


def download_page(root_dir: str, url: str) -> str:
    """
    Download page from URL with resources.

    Args:
        root_dir: directory to download
        url: URL

    Returns:
        str:
    """
    page_name = '{name}.html'.format(name=convert_name(url))
    response = send_request(url)
    resources_dir_name = '{name}_files'.format(name=convert_name(url))
    resources_dir = create_directory(
        root_dir,
        resources_dir_name,
    )
    page, resources_page = parse_page(response.data, url, resources_dir_name)
    write_file(join(root_dir, page_name), page, response.binary)
    for resource in resources_page:
        with suppress(RequestException, HTTPError, OSError):
            resource_response = send_request(resource['link'])

            write_file(
                join(resources_dir, resource['filename']),
                resource_response.data,
                resource_response.binary,
            )
    return page_name


def parse_page(page: str, url: str, resources_dir_name: str) -> tuple:
    """
    Parse page and change links.

    Args:
        page: page
        url: URL
        resources_dir_name: directory name for resources

    Returns:
        tuple: include parsed page and list with links
    """
    root_parse_url = parse_url(url)

    resources_links = []
    already_exists_links = set()
    soup = Bs(page, 'html5lib')
    for tag in soup.find_all(TAGS):
        attr_value = tag.get(TAGS[tag.name])
        if attr_value is None:
            continue

        source_parse_url = parse_url(attr_value)
        if not source_parse_url.netloc:
            source_link = urljoin(url, attr_value)
        elif root_parse_url.netloc == source_parse_url.netloc:
            source_link = attr_value
        else:
            continue

        changed_name = convert_name(url=source_link, parse_extension=True)
        changed_link = join(
            resources_dir_name,
            changed_name,
        )
        tag[TAGS[tag.name]] = '{source}'.format(source=changed_link)

        if source_link in already_exists_links:
            continue
        already_exists_links.add(source_link)

        resources_links.append({
            'tag': tag.name,
            'link': source_link,
            'filename': changed_name,
        })

    return str(soup), resources_links


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


def send_request(url: str) -> namedtuple:
    """
    Send request to url.

    Args:
        url: url

    Raises:
        RequestException: error send request

    Returns:
        namedtuple:
    """
    try:
        response = get(url)
    except RequestException as error:
        raise RequestException(ERROR_REQUEST.format(url=url, error=error))

    if response.status_code != SUCCESSFUL_STATUS_CODE:
        response.raise_for_status()

    if response.encoding:
        return namedtuple('Response', ['data', 'binary', 'url'])(
            data=response.content,
            binary=False,
            url=response.url,
        )
    return namedtuple('Response', ['data', 'binary', 'url'])(
        data=response.text,
        binary=True,
        url=response.url,
    )
