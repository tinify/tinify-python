# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
from tinify import Result


@pytest.fixture
def result_with_meta_and_data():
    return Result(
        {
            "Image-Width": "100",
            "Image-Height": "60",
            "Content-Length": "450",
            "Content-Type": "image/png",
        },
        b"image data",
    )


@pytest.fixture
def result_without_meta_and_data():
    return Result({}, None)


class TestTinifyResultWithMetaAndData:
    def test_width_should_return_image_width(self, result_with_meta_and_data):
        assert 100 == result_with_meta_and_data.width

    def test_height_should_return_image_height(self, result_with_meta_and_data):
        assert 60 == result_with_meta_and_data.height

    def test_location_should_return_none(self, result_with_meta_and_data):
        assert None is result_with_meta_and_data.location

    def test_size_should_return_content_length(self, result_with_meta_and_data):
        assert 450 == result_with_meta_and_data.size

    def test_len_builtin_should_return_content_length(self, result_with_meta_and_data):
        assert 450 == len(result_with_meta_and_data)

    def test_content_type_should_return_mime_type(self, result_with_meta_and_data):
        assert "image/png" == result_with_meta_and_data.content_type

    def test_to_buffer_should_return_image_data(self, result_with_meta_and_data):
        assert b"image data" == result_with_meta_and_data.to_buffer()

    def test_extension(self, result_with_meta_and_data):
        assert "png" == result_with_meta_and_data.extension


class TestTinifyResultWithoutMetaAndData:
    def test_width_should_return_none(self, result_without_meta_and_data):
        assert None is result_without_meta_and_data.width

    def test_height_should_return_none(self, result_without_meta_and_data):
        assert None is result_without_meta_and_data.height

    def test_location_should_return_none(self, result_without_meta_and_data):
        assert None is result_without_meta_and_data.location

    def test_size_should_return_none(self, result_without_meta_and_data):
        assert None is result_without_meta_and_data.size

    def test_len_builtin_should_return_zero(self, result_without_meta_and_data):
        assert 0 == len(result_without_meta_and_data)

    def test_content_type_should_return_none(self, result_without_meta_and_data):
        assert None is result_without_meta_and_data.content_type

    def test_to_buffer_should_return_none(self, result_without_meta_and_data):
        assert None is result_without_meta_and_data.to_buffer()

    def test_extension(self, result_without_meta_and_data):
        assert None is result_without_meta_and_data.extension
