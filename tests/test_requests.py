"""Test requests."""

import pytest
import requests_mock
from page_loader.engine import build_link, send_request
from page_loader.logging import KnownError
from requests.exceptions import HTTPError, RequestException

URL = 'http://test.com'
SERVER_ERROR = 500


def test_successful_answer():
    """Test successful answer."""
    expected = b'data'
    with requests_mock.mock() as mock:
        mock.get(URL, content=b'data')
        assert send_request(URL) == expected


def test_raises_exception_server_error():
    """Test raise exception when server error."""
    with requests_mock.mock() as mock:
        mock.get(URL, status_code=SERVER_ERROR)
        with pytest.raises(HTTPError):
            send_request(URL)


def test_raises_exception_connection_error():
    """Test raise exception when request error."""
    with requests_mock.mock() as mock:
        mock.request(requests_mock.ANY, requests_mock.ANY, exc=RequestException)
        with pytest.raises(KnownError):
            send_request(URL)


@pytest.mark.parametrize(
    'root_url, src_url, expected', [
        (
            'http://test.com/test',
            '//test.com/images/python.png',
            'http://test.com/images/python.png',
        ),
        (
            'http://test.com/test',
            'http://diff_domen.com/python.png',
            None,
        ),
        (
            'http://test.com/blog/',
            'photos/image.png',
            'http://test.com/blog/photos/image.png',
        ),
        (
            'http://test.com/blog/',
            '/photos/image.png',
            'http://test.com/photos/image.png',
        ),
    ],
)
def test_build_link(root_url, src_url, expected):
    """
    Check build link.

    Args:
        root_url: root URL
        src_url:  source URL
        expected: expected link
    """
    assert build_link(root_url, src_url) == expected
