[<img src="https://travis-ci.org/tinify/tinify-python.svg?branch=master" alt="Build Status">](https://travis-ci.org/tinify/tinify-python)

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
nosetests
```

### Integration tests

```
pip install -r requirements.txt -r test-requirements.txt
TINIFY_KEY=$YOUR_API_KEY nosetests test/integration.py
```

## License

This software is licensed under the MIT License. [View the license](LICENSE).
