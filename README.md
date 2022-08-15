[![MIT License](http://img.shields.io/badge/license-MIT-green.svg) ](https://github.com/tinify/tinify-python/blob/main/LICENSE)
[![CI](https://github.com/tinify/tinify-python/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/tinify/tinify-python/actions/workflows/ci-cd.yml)
![PyPI](https://img.shields.io/pypi/v/tinify)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinify)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/tinify)


# Tinify API client for Python

Python client for the Tinify API, used for [TinyPNG](https://tinypng.com) and [TinyJPG](https://tinyjpg.com). Tinify compresses your images intelligently. Read more at [http://tinify.com](http://tinify.com).

## Documentation

[Go to the documentation for the Python client](https://tinypng.com/developers/reference/python).

## Installation

Install the API client:

```
pip install tinify
```

## Usage

```python
import tinify
tinify.key = 'YOUR_API_KEY'

tinify.from_file('unoptimized.png').to_file('optimized.png')
```

## Running tests

```
pip install -r requirements.txt -r test-requirements.txt
py.test
```

To test more runtimes, tox can be used

```
tox
```



### Integration tests

```
pip install -r requirements.txt -r test-requirements.txt
TINIFY_KEY=$YOUR_API_KEY py.test test/integration.py
```

## License

This software is licensed under the MIT License. [View the license](LICENSE).
