[<img src="https://travis-ci.org/tinify/tinify-python.svg?branch=master" alt="Build Status">](https://travis-ci.org/tinify/tinify-python)

# Tinify API client for Python

Python client for the Tinify API. Tinify compresses your images intelligently. Read more at https://tinify.com.

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

## License

This software is licensed under the MIT License. [View the license](LICENSE).
