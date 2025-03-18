# -*- coding: utf-8 -*-
import pytest
from tinify import ResultMeta


@pytest.fixture
def result_with_meta():
    """Fixture that returns a ResultMeta instance with metadata"""
    return ResultMeta(
        {
            "Image-Width": "100",
            "Image-Height": "60",
            "Content-Length": "20",
            "Content-Type": "application/json",
            "Location": "https://bucket.s3-region.amazonaws.com/some/location",
        }
    )


@pytest.fixture
def result_without_meta():
    """Fixture that returns a ResultMeta instance without metadata"""
    return ResultMeta({})


# Tests for ResultMeta with metadata
def test_width_should_return_image_width(result_with_meta):
    assert 100 == result_with_meta.width


def test_height_should_return_image_height(result_with_meta):
    assert 60 == result_with_meta.height


def test_location_should_return_stored_location(result_with_meta):
    assert (
        "https://bucket.s3-region.amazonaws.com/some/location"
        == result_with_meta.location
    )


# Tests for ResultMeta without metadata
def test_width_should_return_none_when_no_meta(result_without_meta):
    assert None is result_without_meta.width


def test_height_should_return_none_when_no_meta(result_without_meta):
    assert None is result_without_meta.height


def test_location_should_return_none_when_no_meta(result_without_meta):
    assert None is result_without_meta.location
