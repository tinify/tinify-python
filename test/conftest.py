import pytest
import os
import tinify
import requests_mock


@pytest.fixture
def dummy_file():
    return os.path.join(os.path.dirname(__file__), "examples", "dummy.png")


@pytest.fixture(autouse=True)
def reset_tinify():
    original_key = tinify.key
    original_app_identifier = tinify.app_identifier
    original_proxy = tinify.proxy

    tinify.key = None
    tinify.app_identifier = None
    tinify.proxy = None

    yield

    tinify.key = original_key
    tinify.app_identifier = original_app_identifier
    tinify.proxy = original_proxy


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker(real_http=False) as m:
        yield m
