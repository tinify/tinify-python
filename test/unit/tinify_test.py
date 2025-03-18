import pytest
import tinify
import base64


def test_key_should_reset_client_with_new_key(mock_requests):
    mock_requests.get("https://api.tinify.com/")
    tinify.key = "abcde"
    tinify.get_client()
    tinify.key = "fghij"
    tinify.get_client().request("GET", "/")

    # Get the last request made to the endpoint
    request = mock_requests.last_request
    assert request.headers["authorization"] == "Basic {0}".format(
        base64.b64encode(b"api:fghij").decode("ascii")
    )


def test_app_identifier_should_reset_client_with_new_app_identifier(mock_requests):
    mock_requests.get("https://api.tinify.com/")
    tinify.key = "abcde"
    tinify.app_identifier = "MyApp/1.0"
    tinify.get_client()
    tinify.app_identifier = "MyApp/2.0"
    tinify.get_client().request("GET", "/")

    request = mock_requests.last_request
    assert request.headers["user-agent"] == tinify.Client.USER_AGENT + " MyApp/2.0"


def test_proxy_should_reset_client_with_new_proxy(mock_requests):
    mock_requests.get("https://api.tinify.com/")

    tinify.key = "abcde"
    tinify.proxy = "http://localhost:8080"
    tinify.get_client()

    tinify.proxy = "http://localhost:9090"
    new_client = tinify.get_client()

    new_client.request("GET", "/")

    # Verify the request was made with the correct proxy configuration
    # The proxy settings should be in the session's proxies attribute
    assert new_client.session.proxies["https"] == "http://localhost:9090"


def test_client_with_key_should_return_client():
    tinify.key = "abcde"
    assert isinstance(tinify.get_client(), tinify.Client)


def test_client_without_key_should_raise_error():
    tinify.key = None
    with pytest.raises(tinify.AccountError):
        tinify.get_client()


def test_client_with_invalid_proxy_should_raise_error(mock_requests):
    # We can test invalid proxy format, but not actual connection issues with requests-mock
    tinify.key = "abcde"
    tinify.proxy = "http-bad-url"  # Invalid proxy URL format

    with pytest.raises(tinify.ConnectionError):
        tinify.get_client().request("GET", "/")


def test_validate_with_valid_key_should_return_true(mock_requests):
    mock_requests.post(
        "https://api.tinify.com/shrink",
        status_code=400,
        json={"error": "Input missing", "message": "No input"},
    )

    tinify.key = "valid"
    assert tinify.validate() is True


def test_validate_with_limited_key_should_return_true(mock_requests):
    mock_requests.post(
        "https://api.tinify.com/shrink",
        status_code=429,
        json={
            "error": "Too many requests",
            "message": "Your monthly limit has been exceeded",
        },
    )

    tinify.key = "valid"
    assert tinify.validate() is True


def test_validate_with_error_should_raise_error(mock_requests):
    mock_requests.post(
        "https://api.tinify.com/shrink",
        status_code=401,
        json={"error": "Unauthorized", "message": "Credentials are invalid"},
    )

    tinify.key = "valid"
    with pytest.raises(tinify.AccountError):
        tinify.validate()


def test_from_file_should_return_source(mock_requests, tmp_path):
    # Create a dummy file
    dummy_file = tmp_path / "test.png"
    dummy_file.write_bytes(b"png file")

    # Mock the API endpoint
    mock_requests.post(
        "https://api.tinify.com/shrink",
        status_code=201,  # Created
        headers={"Location": "https://api.tinify.com/some/location"},
    )

    tinify.key = "valid"
    result = tinify.from_file(str(dummy_file))
    assert isinstance(result, tinify.Source)


def test_from_buffer_should_return_source(mock_requests):
    mock_requests.post(
        "https://api.tinify.com/shrink",
        status_code=201,  # Created
        headers={"Location": "https://api.tinify.com/some/location"},
    )

    tinify.key = "valid"
    result = tinify.from_buffer("png file")
    assert isinstance(result, tinify.Source)


def test_from_url_should_return_source(mock_requests):
    mock_requests.post(
        "https://api.tinify.com/shrink",
        status_code=201,  # Created
        headers={"Location": "https://api.tinify.com/some/location"},
    )

    tinify.key = "valid"
    result = tinify.from_url("http://example.com/test.jpg")
    assert isinstance(result, tinify.Source)
