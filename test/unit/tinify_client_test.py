import pytest
import requests
import json
import base64
import tinify
from tinify import Client, ClientError, ServerError, ConnectionError, AccountError

Client.RETRY_DELAY = 10


def b64encode(data):
    return base64.b64encode(data)


@pytest.fixture
def client():
    return Client("key")


class TestClientRequestWhenValid:
    def test_should_issue_request(self, mock_requests, client):
        mock_requests.get(
            "https://api.tinify.com/", headers={"compression-count": "12"}
        )

        client.request("GET", "/")

        request = mock_requests.last_request
        auth_header = "Basic {0}".format(b64encode(b"api:key").decode("ascii"))
        assert request.headers["authorization"] == auth_header

    def test_should_issue_request_without_body_when_options_are_empty(
        self, mock_requests, client
    ):
        mock_requests.get(
            "https://api.tinify.com/", headers={"compression-count": "12"}
        )

        client.request("GET", "/", {})

        request = mock_requests.last_request
        assert not request.text or request.text == ""

    def test_should_issue_request_without_content_type_when_options_are_empty(
        self, mock_requests, client
    ):
        mock_requests.get(
            "https://api.tinify.com/", headers={"compression-count": "12"}
        )

        client.request("GET", "/", {})

        request = mock_requests.last_request
        assert "content-type" not in request.headers

    def test_should_issue_request_with_json_body(self, mock_requests, client):
        mock_requests.get(
            "https://api.tinify.com/", headers={"compression-count": "12"}
        )

        client.request("GET", "/", {"hello": "world"})

        request = mock_requests.last_request
        assert request.headers["content-type"] == "application/json"
        assert request.text == '{"hello":"world"}'

    def test_should_issue_request_with_user_agent(self, mock_requests, client):
        mock_requests.get(
            "https://api.tinify.com/", headers={"compression-count": "12"}
        )

        client.request("GET", "/")

        request = mock_requests.last_request
        assert request.headers["user-agent"] == Client.USER_AGENT

    def test_should_update_compression_count(self, mock_requests, client):
        mock_requests.get(
            "https://api.tinify.com/", headers={"compression-count": "12"}
        )

        client.request("GET", "/")

        assert tinify.compression_count == 12


class TestClientRequestWhenValidWithAppId:
    def test_should_issue_request_with_user_agent(self, mock_requests):
        mock_requests.get(
            "https://api.tinify.com/", headers={"compression-count": "12"}
        )

        Client("key", "TestApp/0.2").request("GET", "/")

        request = mock_requests.last_request
        assert request.headers["user-agent"] == Client.USER_AGENT + " TestApp/0.2"


class TestClientRequestWhenValidWithProxy:
    @pytest.mark.skip(
        reason="requests does not set a proxy unless a real proxy is used"
    )
    def test_should_issue_request_with_proxy_authorization(self, mock_requests):
        proxy_url = "http://user:pass@localhost:8080"
        expected_auth = "Basic " + base64.b64encode(b"user:pass").decode()

        mock_requests.get("https://api.tinify.com/", status_code=200)

        client = Client("key", None, proxy_url)
        client.request("GET", "/")

        # Verify the last request captured by requests-mock
        last_request = mock_requests.last_request
        assert last_request is not None
        assert last_request.headers.get("Proxy-Authorization") == expected_auth


class TestClientRequestWithTimeout:
    def test_should_raise_connection_error_repeatedly(self, mock_requests):
        mock_requests.get(
            "https://api.tinify.com/",
            [
                {"exc": requests.exceptions.Timeout},
            ],
        )
        with pytest.raises(ConnectionError) as excinfo:
            Client("key").request("GET", "/")
        assert str(excinfo.value) == "Timeout while connecting"
        assert isinstance(excinfo.value.__cause__, requests.exceptions.Timeout)

    def test_should_issue_request_after_timeout_once(self, mock_requests):
        # Confirm retry happens after timeout
        mock_requests.get(
            "https://api.tinify.com/",
            [
                {"exc": requests.exceptions.Timeout("Timeout")},
                {
                    "status_code": 201,
                    "headers": {"compression-count": "12"},
                    "text": "success",
                },
            ],
        )

        result = Client("key").request("GET", "/", {})

        assert result.status_code == 201
        assert mock_requests.call_count == 2  # Verify retry happened


class TestClientRequestWithConnectionError:
    def test_should_raise_connection_error_repeatedly(self, mock_requests):
        mock_requests.get(
            "https://api.tinify.com/",
            [
                {"exc": requests.exceptions.ConnectionError("connection error")},
            ],
        )
        with pytest.raises(ConnectionError) as excinfo:
            Client("key").request("GET", "/")
        assert str(excinfo.value) == "Error while connecting: connection error"
        assert isinstance(excinfo.value.__cause__, requests.exceptions.ConnectionError)

    def test_should_issue_request_after_connection_error_once(self, mock_requests):
        # Mock the request to fail with ConnectionError once, then succeed
        mock_requests.get(
            "https://api.tinify.com/",
            [
                {"exc": requests.exceptions.ConnectionError},  # First attempt fails
                {
                    "status_code": 201,
                    "headers": {"compression-count": "12"},
                    "text": "success",
                },  # Second attempt succeeds
            ],
        )

        client = Client("key")
        result = client.request("GET", "/", {})

        # Verify results
        assert result.status_code == 201
        assert mock_requests.call_count == 2  # Ensure it retried


class TestClientRequestWithSomeError:
    def test_should_raise_connection_error_repeatedly(self, mock_requests):
        mock_requests.get(
            "https://api.tinify.com/",
            [
                {"exc": RuntimeError("some error")},
            ],
        )
        with pytest.raises(ConnectionError) as excinfo:
            Client("key").request("GET", "/")
        assert str(excinfo.value) == "Error while connecting: some error"

    def test_should_issue_request_after_some_error_once(self, mock_requests):
        # Mock the request to fail with RuntimeError once, then succeed
        mock_requests.get(
            "https://api.tinify.com/",
            [
                {"exc": RuntimeError("some error")},  # First attempt fails
                {
                    "status_code": 201,
                    "headers": {"compression-count": "12"},
                    "text": "success",
                },  # Second attempt succeeds
            ],
        )

        client = Client("key")
        result = client.request("GET", "/", {})

        # Verify results
        assert result.status_code == 201
        assert mock_requests.call_count == 2  # Ensure it retried


class TestClientRequestWithServerError:
    def test_should_raise_server_error_repeatedly(self, mock_requests):
        error_body = json.dumps({"error": "InternalServerError", "message": "Oops!"})
        mock_requests.get("https://api.tinify.com/", status_code=584, text=error_body)

        with pytest.raises(ServerError) as excinfo:
            Client("key").request("GET", "/")
        assert str(excinfo.value) == "Oops! (HTTP 584/InternalServerError)"

    def test_should_issue_request_after_server_error_once(self, mock_requests):
        error_body = json.dumps({"error": "InternalServerError", "message": "Oops!"})
        # First call returns error, second succeeds
        mock_requests.register_uri(
            "GET",
            "https://api.tinify.com/",
            [
                {"status_code": 584, "text": error_body},
                {"status_code": 201, "text": "all good"},
            ],
        )

        response = Client("key").request("GET", "/")

        assert response.status_code == 201


class TestClientRequestWithBadServerResponse:
    def test_should_raise_server_error_repeatedly(self, mock_requests):
        mock_requests.get(
            "https://api.tinify.com/", status_code=543, text="<!-- this is not json -->"
        )

        with pytest.raises(ServerError) as excinfo:
            Client("key").request("GET", "/")
        # Using pytest's assert to check regex pattern
        error_message = str(excinfo.value)
        assert "Error while parsing response:" in error_message
        assert "(HTTP 543/ParseError)" in error_message

    def test_should_issue_request_after_bad_response_once(self, mock_requests):
        # First call returns invalid JSON, second succeeds
        mock_requests.register_uri(
            "GET",
            "https://api.tinify.com/",
            [
                {"status_code": 543, "text": "<!-- this is not json -->"},
                {"status_code": 201, "text": "all good"},
            ],
        )

        response = Client("key").request("GET", "/")

        assert response.status_code == 201


class TestClientRequestWithClientError:
    def test_should_raise_client_error(self, mock_requests):
        error_body = json.dumps({"error": "BadRequest", "message": "Oops!"})
        mock_requests.get("https://api.tinify.com/", status_code=492, text=error_body)

        with pytest.raises(ClientError) as excinfo:
            Client("key").request("GET", "/")
        assert str(excinfo.value) == "Oops! (HTTP 492/BadRequest)"


class TestClientRequestWithBadCredentialsResponse:
    def test_should_raise_account_error(self, mock_requests):
        error_body = json.dumps({"error": "Unauthorized", "message": "Oops!"})
        mock_requests.get("https://api.tinify.com/", status_code=401, text=error_body)

        with pytest.raises(AccountError) as excinfo:
            Client("key").request("GET", "/")
        assert str(excinfo.value) == "Oops! (HTTP 401/Unauthorized)"
