import sys
import os
from contextlib import contextmanager
import tinify
import pytest
import tempfile

if not os.environ.get("TINIFY_KEY"):
    sys.exit("Set the TINIFY_KEY environment variable.")


@contextmanager
def create_named_tmpfile():
    #  Due to NamedTemporaryFile requiring to be closed when used on Windows
    #   we create our own NamedTemporaryFile contextmanager
    # See note: https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile

    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp.close()
        yield tmp.name
    finally:
        os.unlink(tmp.name)


# Fixture for shared resources
@pytest.fixture(scope="module")
def optimized_image():
    tinify.key = os.environ.get("TINIFY_KEY")
    tinify.proxy = os.environ.get("TINIFY_PROXY")

    unoptimized_path = os.path.join(
        os.path.dirname(__file__), "examples", "voormedia.png"
    )
    return tinify.from_file(unoptimized_path)


def test_should_compress_from_file(optimized_image):
    with create_named_tmpfile() as tmp:
        optimized_image.to_file(tmp)

        size = os.path.getsize(tmp)

        with open(tmp, "rb") as f:
            contents = f.read()

        assert 1000 < size < 1500

        # width == 137
        assert b"\x00\x00\x00\x89" in contents
        assert b"Copyright Voormedia" not in contents


def test_should_compress_from_url():
    source = tinify.from_url(
        "https://raw.githubusercontent.com/tinify/tinify-python/master/test/examples/voormedia.png"
    )
    with create_named_tmpfile() as tmp:
        source.to_file(tmp)

        size = os.path.getsize(tmp)
        with open(tmp, "rb") as f:
            contents = f.read()

        assert 1000 < size < 1500

        # width == 137
        assert b"\x00\x00\x00\x89" in contents
        assert b"Copyright Voormedia" not in contents


def test_should_resize(optimized_image):
    with create_named_tmpfile() as tmp:
        optimized_image.resize(method="fit", width=50, height=20).to_file(tmp)

        size = os.path.getsize(tmp)
        with open(tmp, "rb") as f:
            contents = f.read()

        assert 500 < size < 1000

        # width == 50
        assert b"\x00\x00\x00\x32" in contents
        assert b"Copyright Voormedia" not in contents


def test_should_preserve_metadata(optimized_image):
    with create_named_tmpfile() as tmp:
        optimized_image.preserve("copyright", "creation").to_file(tmp)

        size = os.path.getsize(tmp)
        with open(tmp, "rb") as f:
            contents = f.read()

        assert 1000 < size < 2000

        # width == 137
        assert b"\x00\x00\x00\x89" in contents
        assert b"Copyright Voormedia" in contents


def test_should_transcode_image(optimized_image):
    with create_named_tmpfile() as tmp:
        optimized_image.convert(type=["image/webp"]).to_file(tmp)
        with open(tmp, "rb") as f:
            content = f.read()

        assert b"RIFF" == content[:4]
        assert b"WEBP" == content[8:12]
