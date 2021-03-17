"""Test requests."""

import pytest
import requests_mock
from page_loader.engine import send_request
from requests.exceptions import HTTPError, RequestException

URL = 'http://test.com/'
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
        with pytest.raises(RequestException):
            send_request(URL)
