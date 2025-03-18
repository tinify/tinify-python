# -*- coding: utf-8 -*-
import os
import json
import tempfile
import pytest

import tinify
from tinify import Source, Result, ResultMeta, AccountError, ClientError


def create_named_tmpfile():
    """Helper to create a named temporary file"""
    fd, name = tempfile.mkstemp()
    os.close(fd)
    return name


def assert_json_equal(expected, actual):
    """Helper to assert JSON equality"""
    if isinstance(actual, str):
        actual = json.loads(actual)
    if isinstance(expected, str):
        expected = json.loads(expected)
    assert expected == actual


class TestTinifySourceWithInvalidApiKey:
    @pytest.fixture(autouse=True)
    def setup(self, mock_requests):
        tinify.key = "invalid"
        mock_requests.post("https://api.tinify.com/shrink", status_code=401)
        yield

    def test_from_file_should_raise_account_error(self, dummy_file):
        with pytest.raises(AccountError):
            Source.from_file(dummy_file)

    def test_from_buffer_should_raise_account_error(self):
        with pytest.raises(AccountError):
            Source.from_buffer("png file")

    def test_from_url_should_raise_account_error(self):
        with pytest.raises(AccountError):
            Source.from_url("http://example.com/test.jpg")


class TestTinifySourceWithValidApiKey:
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mock_requests):
        tinify.key = "valid"
        mock_requests.post(
            "https://api.tinify.com/shrink",
            status_code=201,
            headers={"location": "https://api.tinify.com/some/location"},
        )
        mock_requests.get(
            "https://api.tinify.com/some/location", content=self.return_file
        )
        mock_requests.post(
            "https://api.tinify.com/some/location", content=self.return_file
        )
        yield

    def return_file(self, request, context):
        data = request.json() if request.body else {}
        if "store" in data:
            context.headers["location"] = (
                "https://bucket.s3-region.amazonaws.com/some/location"
            )
            return json.dumps({"status": "success"}).encode("utf-8")
        elif "preserve" in data:
            return b"copyrighted file"
        elif "resize" in data:
            return b"small file"
        elif "convert" in data:
            return b"converted file"
        elif "transform" in data:
            return b"transformed file"
        else:
            return b"compressed file"

    def test_from_file_with_path_should_return_source(self, dummy_file):
        assert isinstance(Source.from_file(dummy_file), Source)

    def test_from_file_with_path_should_return_source_with_data(self, dummy_file):
        assert b"compressed file" == Source.from_file(dummy_file).to_buffer()

    def test_from_file_with_file_object_should_return_source(self, dummy_file):
        with open(dummy_file, "rb") as f:
            assert isinstance(Source.from_file(f), Source)

    def test_from_file_with_file_object_should_return_source_with_data(
        self, dummy_file
    ):
        with open(dummy_file, "rb") as f:
            assert b"compressed file" == Source.from_file(f).to_buffer()

    def test_from_buffer_should_return_source(self):
        assert isinstance(Source.from_buffer("png file"), Source)

    def test_from_buffer_should_return_source_with_data(self):
        assert b"compressed file" == Source.from_buffer("png file").to_buffer()

    def test_from_url_should_return_source(self):
        assert isinstance(Source.from_url("http://example.com/test.jpg"), Source)

    def test_from_url_should_return_source_with_data(self):
        assert (
            b"compressed file"
            == Source.from_url("http://example.com/test.jpg").to_buffer()
        )

    def test_from_url_should_raise_error_when_server_doesnt_return_a_success(
        self, mock_requests
    ):
        mock_requests.post(
            "https://api.tinify.com/shrink",
            json={"error": "Source not found", "message": "Cannot parse URL"},
            status_code=400,
        )
        with pytest.raises(ClientError):
            Source.from_url("file://wrong")

    def test_result_should_return_result(self):
        assert isinstance(Source.from_buffer(b"png file").result(), Result)

    def test_preserve_should_return_source(self, mock_requests):
        assert isinstance(
            Source.from_buffer(b"png file").preserve("copyright", "location"), Source
        )
        assert b"png file" == mock_requests.last_request.body

    def test_preserve_should_return_source_with_data(self, mock_requests):
        assert (
            b"copyrighted file"
            == Source.from_buffer(b"png file")
            .preserve("copyright", "location")
            .to_buffer()
        )
        assert_json_equal(
            '{"preserve":["copyright","location"]}', mock_requests.last_request.json()
        )

    def test_preserve_should_return_source_with_data_for_array(self, mock_requests):
        assert (
            b"copyrighted file"
            == Source.from_buffer(b"png file")
            .preserve(["copyright", "location"])
            .to_buffer()
        )
        assert_json_equal(
            '{"preserve":["copyright","location"]}', mock_requests.last_request.json()
        )

    def test_preserve_should_return_source_with_data_for_tuple(self, mock_requests):
        assert (
            b"copyrighted file"
            == Source.from_buffer(b"png file")
            .preserve(("copyright", "location"))
            .to_buffer()
        )
        assert_json_equal(
            '{"preserve":["copyright","location"]}', mock_requests.last_request.json()
        )

    def test_preserve_should_include_other_options_if_set(self, mock_requests):
        assert (
            b"copyrighted file"
            == Source.from_buffer(b"png file")
            .resize(width=400)
            .preserve("copyright", "location")
            .to_buffer()
        )
        assert_json_equal(
            '{"preserve":["copyright","location"],"resize":{"width":400}}',
            mock_requests.last_request.json(),
        )

    def test_resize_should_return_source(self, mock_requests):
        assert isinstance(Source.from_buffer(b"png file").resize(width=400), Source)
        assert b"png file" == mock_requests.last_request.body

    def test_resize_should_return_source_with_data(self, mock_requests):
        assert (
            b"small file"
            == Source.from_buffer(b"png file").resize(width=400).to_buffer()
        )
        assert_json_equal('{"resize":{"width":400}}', mock_requests.last_request.json())

    def test_transform_should_return_source(self, mock_requests):
        assert isinstance(
            Source.from_buffer(b"png file").transform(background="black"), Source
        )
        assert b"png file" == mock_requests.last_request.body

    def test_transform_should_return_source_with_data(self, mock_requests):
        assert (
            b"transformed file"
            == Source.from_buffer(b"png file").transform(background="black").to_buffer()
        )
        assert_json_equal(
            '{"transform":{"background":"black"}}', mock_requests.last_request.json()
        )

    def test_convert_should_return_source(self, mock_requests):
        assert isinstance(
            Source.from_buffer(b"png file")
            .resize(width=400)
            .convert(type=["image/webp"]),
            Source,
        )
        assert b"png file" == mock_requests.last_request.body

    def test_convert_should_return_source_with_data(self, mock_requests):
        assert (
            b"converted file"
            == Source.from_buffer(b"png file").convert(type="image/jpg").to_buffer()
        )
        assert_json_equal(
            '{"convert": {"type": "image/jpg"}}', mock_requests.last_request.json()
        )

    def test_store_should_return_result_meta(self, mock_requests):
        assert isinstance(
            Source.from_buffer(b"png file").store(service="s3"), ResultMeta
        )
        assert_json_equal(
            '{"store":{"service":"s3"}}', mock_requests.last_request.json()
        )

    def test_store_should_return_result_meta_with_location(self, mock_requests):
        assert (
            "https://bucket.s3-region.amazonaws.com/some/location"
            == Source.from_buffer(b"png file").store(service="s3").location
        )
        assert_json_equal(
            '{"store":{"service":"s3"}}', mock_requests.last_request.json()
        )

    def test_store_should_include_other_options_if_set(self, mock_requests):
        assert (
            "https://bucket.s3-region.amazonaws.com/some/location"
            == Source.from_buffer(b"png file")
            .resize(width=400)
            .store(service="s3")
            .location
        )
        assert_json_equal(
            '{"store":{"service":"s3"},"resize":{"width":400}}',
            mock_requests.last_request.json(),
        )

    def test_to_buffer_should_return_image_data(self):
        assert b"compressed file" == Source.from_buffer(b"png file").to_buffer()

    def test_to_file_with_path_should_store_image_data(self):
        with tempfile.TemporaryFile() as tmp:
            Source.from_buffer(b"png file").to_file(tmp)
            tmp.seek(0)
            assert b"compressed file" == tmp.read()

    def test_to_file_with_file_object_should_store_image_data(self):
        name = create_named_tmpfile()
        try:
            Source.from_buffer(b"png file").to_file(name)
            with open(name, "rb") as f:
                assert b"compressed file" == f.read()
        finally:
            os.unlink(name)

    def test_all_options_together(self, mock_requests):
        assert (
            "https://bucket.s3-region.amazonaws.com/some/location"
            == Source.from_buffer(b"png file")
            .resize(width=400)
            .convert(type=["image/webp", "image/png"])
            .transform(background="black")
            .preserve("copyright", "location")
            .store(service="s3")
            .location
        )
        assert_json_equal(
            '{"store":{"service":"s3"},"resize":{"width":400},"preserve": ["copyright", "location"], "transform": {"background": "black"}, "convert": {"type": ["image/webp", "image/png"]}}',
            mock_requests.last_request.json(),
        )
