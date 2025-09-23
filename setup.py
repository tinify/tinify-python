import sys
import os
import re
import io

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tinify"))
from version import __version__

install_require = ["requests >= 2.7.0, < 3.0.0"]
tests_require = ["pytest", "pytest-xdist", "requests-mock", "types-requests"]

if sys.version_info.major > 2:
    tests_require.append("mypy")

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tinify",
    version=__version__,
    description="Tinify API client.",
    author="Jacob Middag",
    author_email="info@tinify.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://tinify.com/developers",
    packages=["tinify"],
    package_data={
        "": ["LICENSE", "README.md"],
        "tinify": ["data/cacert.pem", "py.typed"],
    },
    install_requires=install_require,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ),
)
