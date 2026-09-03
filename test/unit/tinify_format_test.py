# -*- coding: utf-8 -*-
import json
import pytest

import tinify
from tinify import Format, Source


class TestTinifyFormat:
    def test_should_expose_supported_media_types(self):
        assert Format.WEBP == "image/webp"
        assert Format.PNG == "image/png"
        assert Format.JPEG == "image/jpeg"
        assert Format.JPG == "image/jpg"
        assert Format.AVIF == "image/avif"
        assert Format.JXL == "image/jxl"
        assert Format.ANY == "*/*"

    def test_should_not_be_instantiable(self):
        with pytest.raises(TypeError):
            Format()


class TestTinifyFormatConvert:
    @pytest.fixture(autouse=True)
    def setup(self, mock_requests):
        tinify.key = "valid"
        mock_requests.post(
            "https://api.tinify.com/shrink",
            status_code=201,
            headers={"Location": "https://api.tinify.com/some/location"},
        )
        self.mock_requests = mock_requests
        yield

    def test_convert_with_format_should_serialize_media_type(self):
        self.mock_requests.post(
            "https://api.tinify.com/some/location",
            status_code=200,
            content=b"converted file",
        )

        Source.from_buffer("png file").convert(type=Format.JXL).to_buffer()

        body = json.loads(self.mock_requests.last_request.text)
        assert body["convert"] == {"type": "image/jxl"}

    def test_convert_with_multiple_formats_should_serialize_media_types(self):
        self.mock_requests.post(
            "https://api.tinify.com/some/location",
            status_code=200,
            content=b"converted file",
        )

        Source.from_buffer("png file").convert(
            type=[Format.JXL, Format.WEBP]
        ).to_buffer()

        body = json.loads(self.mock_requests.last_request.text)
        assert body["convert"] == {"type": ["image/jxl", "image/webp"]}
